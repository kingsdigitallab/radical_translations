let baseURL = `${window.location.origin}${window.location.pathname}`
if (window.viewBaseURL) {
  baseURL = viewBaseURL
}

new Vue({
  el: '#app',
  components: {
    'vue-slider': window['vue-slider-component']
  },
  delimiters: ['{[', ']}'],
  data: {
    url: new URL(`${baseURL}api/`),
    urlResources: new URL(`${baseURL}../resources/api-simple/`),
    urlSuggest: new URL(`${baseURL}api/suggest/`),
    query: '',
    query_text: '',
    query_dates: [options.year_min, options.year_max],
    has_date_query: false,
    filters: [],
    ordering_default: 'score',
    ordering: 'score',
    ordering_options: [
      { key: 'score', value: 'Relevance' },
      { key: 'title', value: 'Title ascending' },
      { key: '-title', value: 'Title descending' },
      { key: 'year', value: 'Year ascending' },
      { key: '-year', value: 'Year descending' }
    ],
    page: 1,
    page_size: options.page_size !== undefined ? options.page_size : 50,
    rangeMarks: (v) => v % 10 === 0,
    data: [],
    data_suggest: [],
    map: {
      mapObject: null,
      options: {
        zoomSnap: 0.5
      },
      center: window.L.latLng(53.3439, 0),
      show: false,
      zoom: 4,
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      popup: {
        item: null,
        place: null
      }
    },
    events: { country: null, year: null, data: [], show: false },
    eventsResources: [],
    timeline: {}
  },
  watch: {
    query_text: _.debounce(async function () {
      await this.getSuggestions()
    }, 250),
    page: _.debounce(async function () {
      await this.search()
    }, 250),
    ordering: async function (newOrdering, oldOrdering) {
      await this.search()
    },
    filters: async function (newFilters, oldFilters) {
      this.page = 1
      await this.search()
    },
    'map.show': async function (newShow, oldShow) {
      if (newShow) {
        this.page = 1
        this.page_size = 2000
        dispatchWindowResizeEvent()
        await this.search()
        this.renderMap()
      } else {
        this.page_size = options.page_size
        await this.search()
      }
    }
  },
  created: async function () {
    this.loadSearchParams()
    await this.search()
    this.initMap()
  },
  computed: {
    facets: function () {
      return this.getFacets().filter(
        (f) =>
          ![...options.meta_facets, ...options.range_facets].includes(f.name)
      )
    },
    metaFacets: function () {
      const facets = this.getFacets().filter((f) =>
        options.meta_facets.includes(f.name)
      )
      if (facets.length == 1) {
        return facets[0]
      }

      return facets
    },
    rangeFacets: function () {
      const facets = this.getFacets().filter((f) =>
        options.range_facets.includes(f.name)
      )

      return facets
    },
    numberOfPages: function () {
      return Math.ceil(this.data.count / this.data.page_size)
    },
    suggestions: function () {
      let suggestions = []

      if (this.data_suggest !== undefined) {
        Object.keys(this.data_suggest).forEach((s) => {
          this.data_suggest[s][0].options.forEach((o) =>
            suggestions.push(o.text)
          )
        })
      }

      return suggestions
    },
    eventsChartData: function () {
      if (!this.data || !this.data.results) {
        return {}
      }

      const labels = this.data.facets._filter_country.country.buckets.map(
        (f) => f.key
      )

      events = { labels: labels, datasets: [], annotations: {} }

      colours = {
        Czechia: 'rgba(34, 116, 165, 0.4)',
        Egypt: 'rgba(187, 133, 136, 0.4)',
        France: 'rgba(84, 13, 110, 0.4)',
        Germany: 'rgba(230, 175, 46, 0.4)',
        Ireland: 'rgba(99, 43, 48, 0.4)',
        Italy: 'rgba(11, 3, 45, 0.4)',
        Spain: 'rgba(169, 210, 213, 0.4)',
        'United Kingdom': 'rgba(215, 38, 56, 0.4)',
        'United States': 'rgba(103, 148, 54, 0.4)'
      }

      // for each country
      labels.forEach((country, idx) => {
        const colour = colours[country]

        let dataset = {
          label: country,
          backgroundColor: colour,
          borderColor: colour,
          data: []
        }

        this.data.results.forEach((evt) => {
          // for each event in the country
          if (evt.year && evt.place.country.name === country) {
            evt.year.forEach((year) => {
              dataset.data.push({
                x: year,
                y: idx,
                r: 5,
                meta: {
                  type: 'event',
                  id: evt.id,
                  year: year,
                  place: country,
                  n: 1,
                  resources: evt.related_to.length
                }
              })
            })
          }
        })

        // keep only the first and last items of multi-year events and add annotations
        dataset.data = dataset.data.reduce((acc, cur) => {
          if (acc.filter((item) => item.meta.id === cur.meta.id).length === 2) {
            const start = acc[acc.length - 2]
            acc[acc.length - 1] = cur

            events.annotations[cur.meta.id] = {
              type: 'box',
              id: `${cur.meta.id}`,
              display: true,
              xScaleID: 'x-axis-0',
              yScaleID: 'y-axis-0',
              xMin: start.x,
              yMin: cur.y - 0.1,
              xMax: cur.x,
              yMax: cur.y + 0.1,
              backgroundColor: colour,
              borderWidth: 1
            }

            return acc
          }

          acc.push(cur)

          return acc
        }, [])

        // group the events by year
        dataset.data = dataset.data.reduce((acc, cur) => {
          if (acc.some((item) => item.x === cur.x)) {
            const last = acc.length - 1
            acc[last].r += 2
            acc[last].meta.n += 1
            acc[last].meta.resources += cur.meta.resources
            return acc
          }

          acc.push(cur)

          return acc
        }, [])

        events.datasets.push(dataset)
      })

      if (this.eventsResources && this.eventsResources.facets) {
        const resourcesLabels = this.eventsResources.facets._filter_country.country.buckets
          .map((f) => f.key)
          .filter((f) => f !== 'any')

        resourcesLabels.forEach((country, idx) => {
          let dataset = {
            label: `${country} resources`,
            data: []
          }

          this.eventsResources.results.forEach((res) => {
            const has_country = res.places.filter((place) => {
              return place.place.country !== undefined
                ? place.place.country.name === country
                : false
            })
            if (res.year && has_country.length > 0) {
              res.year.forEach((year) => {
                dataset.data.push({
                  x: year,
                  y: idx + labels.length + 1,
                  r: 5,
                  meta: {
                    type: 'resource',
                    id: res.id,
                    year: year,
                    place: country,
                    n: 1
                  }
                })
              })
            }
          })

          // keep only the first and last items of multi-year resources and add annotations
          dataset.data = dataset.data.reduce((acc, cur) => {
            if (
              acc.filter((item) => item.meta.id === cur.meta.id).length === 2
            ) {
              const start = acc[acc.length - 2]
              acc[acc.length - 1] = cur

              events.annotations[cur.meta.id] = {
                type: 'box',
                id: `${cur.meta.id}`,
                display: true,
                xScaleID: 'x-axis-0',
                yScaleID: 'y-axis-0',
                xMin: start.x,
                yMin: cur.y - 0.1,
                xMax: cur.x,
                yMax: cur.y + 0.1,
                borderWidth: 1
              }

              return acc
            }

            acc.push(cur)

            return acc
          }, [])

          // group the resources by year
          dataset.data = dataset.data.reduce((acc, cur) => {
            if (acc.some((item) => item.x === cur.x)) {
              const last = acc.length - 1
              acc[last].r += 2
              acc[last].meta.n += 1
              return acc
            }

            acc.push(cur)

            return acc
          }, [])

          events.datasets.push(dataset)
        })
      }

      return events
    }
  },
  methods: {
    getFacetDisplayName: function (name) {
      return name.replaceAll('_', ' ')
    },
    clearFilters: function () {
      this.filters = []
      this.page = 1
      this.query = ''
      this.query_dates = [options.year_min, options.year_max]
    },
    getBucketValue: function (bucket) {
      return bucket.key_as_string ? bucket.key_as_string : bucket.key
    },
    getContributions: function (item) {
      return item.contributions
        .filter((c) => c.agent.name !== 'any')
        .map((c) => ({
          agent: c.agent,
          roles: c.roles.filter((r) => r.label !== undefined)
        }))
    },
    getFacets: function () {
      return this.getFacetsCache(this.data)
    },
    getFacetsCache: _.memoize(function (data) {
      let facets = []

      if (data.facets !== undefined) {
        Object.keys(data.facets).forEach((f) => {
          const name = f.replace('_filter_', '')
          const range = name === 'year' ? true : false
          let buckets = data.facets[f][name]['buckets']
          let chartData = {
            labels: [],
            datasets: [
              { label: options.label, backgroundColor: '#9b2923', data: [] }
            ]
          }

          if (range) {
            //buckets = buckets.flatMap((b) => Array(b.doc_count).fill(b.key))
            buckets.findIndex((b) => b.key === options.year_min) === -1
              ? buckets.unshift({ key: options.year_min, count: 0 })
              : buckets
            buckets.findIndex((b) => b.key === options.year_max) === -1
              ? buckets.push({ key: options.year_max })
              : buckets
            chartData.labels = buckets.map((b) => b.key)
            chartData.datasets[0].data = buckets.map((b) => b.doc_count)
          }

          facets.push({
            name: name,
            range: range,
            buckets: buckets,
            chartData: chartData,
            display: this.query_dates
          })
        })
      }

      facets.sort(function (a, b) {
        const nameA = a.name.toUpperCase()
        const nameB = b.name.toUpperCase()

        if (nameA < nameB) {
          return -1
        }
        if (nameA > nameB) {
          return 1
        }

        return 0
      })

      return facets
    }),
    getFacetCount: function (buckets) {
      return buckets
        .map((el) => el.doc_count)
        .reduce((acc, cur) => Math.max(acc, cur), 0)
    },
    getSuggestions: async function () {
      if (!this.query_text) {
        this.data_suggest = []
        return
      }

      const params = new URLSearchParams()
      params.append('suggest_field', this.query_text)

      this.urlSuggest.search = params.toString()
      this.data_suggest = await fetch(this.urlSuggest).then((response) =>
        response.json()
      )
    },
    handleChartClick: async function (from, to) {
      this.query_dates = [from, to]
      await this.rangeSearch()
    },
    hasAny: function (facet) {
      return facet.buckets.find((b) => this.getBucketValue(b) === 'any')
    },
    hasFilter: function (filter) {
      return (
        this.filters.find(
          (item) =>
            item[0] === filter[0] &&
            (filter[1] === undefined || item[1] === filter[1])
        ) !== undefined
      )
    },
    loadSearchParams: function () {
      const params = new URLSearchParams(window.location.search)

      let key = 'page'
      if (params.has(key)) {
        this.page = params.get(key)
        params.delete(key)
      }

      key = 'page_size'
      if (params.has(key)) {
        this.page_size = params.get(key)
        params.delete(key)
      }

      key = 'search'
      if (params.has(key)) {
        this.query = params.get(key)
        params.delete(key)
      }

      key = 'year__gte'
      if (params.has(key)) {
        this.query_dates[0] = params.get(key)
        params.delete(key)
      }

      key = 'year__lte'
      if (params.has(key)) {
        this.query_dates[1] = params.get(key)
        params.delete(key)
      }

      for (const key of params.keys()) {
        this.updateFilters([key.replace('__term', ''), params.get(key)])
      }
    },
    rangeSearch: async function (reset = false) {
      this.page = 1
      if (reset) {
        this.query_dates = [options.year_min, options.year_max]
      }
      await this.search()
    },
    search: async function () {
      this.data = await this.doSearch()

      if (options.resources) {
        this.eventsResources = await this.doSearch(
          this.urlResources,
          1500,
          1750,
          1900
        )
        this.timeline = this.getTimeline()
      }
      if (this.map.show) {
        this.renderMap()
      }
    },
    doSearch: async function (
      url = this.url,
      page_size = this.page_size,
      year_from = this.query_dates[0],
      year_to = this.query_dates[1]
    ) {
      const params = new URLSearchParams()

      if (this.query) {
        params.append('search', this.query)
      }

      if (year_from !== options.year_min) {
        params.append('year__gte', year_from)
      }
      if (year_to !== options.year_max) {
        params.append('year__lte', year_to)
      }

      if (params.has('year__gte') || params.has('year__lte')) {
        this.has_date_query = true
      } else {
        this.has_date_query = false
      }

      if (!this.page || this.page > this.numberOfPages) {
        this.page = 1
      }

      params.append('page', this.page)
      params.append('page_size', page_size)

      if (this.ordering !== this.ordering_default) {
        params.append('ordering', this.ordering)
      }

      this.filters.forEach((filter) =>
        params.append(`${filter[0]}__term`, filter[1])
      )

      url.search = params.toString()
      window.history.pushState({}, '', url.search)

      const response = await fetch(url)

      return response.json()
    },
    textSearch: async function (text) {
      this.page = 1
      this.query = this.query_text
      this.query_text = ''

      if (text) {
        this.query = text
      }

      await this.search()
    },
    updateFilters: function (filter) {
      if (this.hasFilter(filter)) {
        this.filters = this.filters.filter(
          (item) => item[0] !== filter[0] || item[1] !== filter[1]
        )
      } else {
        this.filters.push(filter)
      }
    },
    initMap: async function () {
      if (!document.getElementById('map')) return

      const map = L.map('map')
      map.setView(this.map.center, this.map.zoom)

      L.tileLayer(this.map.url, {
        attribution: this.map.attribution
      }).addTo(map)

      this.map.mapObject = map
    },
    renderMap: function () {
      if (!this.map.mapObject) return

      const map = this.map.mapObject
      const cluster = L.markerClusterGroup()

      const vue = this
      this.data.results.forEach((item) =>
        item[options.map_field].forEach((p) => {
          const place = p.place !== undefined ? p.place : p

          if (place !== undefined) {
            cluster.addLayer(
              L.marker(place.geo).on('click', function () {
                const marker = this

                vue.map.popup.item = item
                vue.map.popup.place = place

                vue.$nextTick(() =>
                  marker
                    .bindPopup(
                      document.getElementById('map-popup-container').innerHTML
                    )
                    .openPopup()
                )
              })
            )
          }
        })
      )

      map.addLayer(cluster)

      map.whenReady(() => map.invalidateSize())
    },
    handleEventClick: function (place, year) {
      this.events.country = place
      this.events.year = year

      const params = new URLSearchParams()
      params.append('country__term', place)
      params.append('year', year)

      this.filters.forEach((filter) =>
        params.append(`${filter[0]}__term`, filter[1])
      )

      const url = this.url
      url.search = params.toString()

      const data = fetch(url)
        .then((response) => response.json())
        .then((data) => {
          this.events.data = data.results
          this.events.show = true
        })
    },
    getTimeline: function () {
      const timeline = {}

      if (!this.data || !this.data.results) {
        return timeline
      }

      const events = this.data.results.flatMap((r) =>
        r.year.map((year) => {
          const record = `event-${r.id}`
          return {
            country: r.place.country.name,
            year: year,
            id: r.id,
            type: 'event',
            record: record,
            title: r.title,
            date: r.date
          }
        })
      )

      let resources = []

      if (this.eventsResources && this.eventsResources.results) {
        resources = this.eventsResources.results.flatMap((r) => {
          return r.places
            .filter(
              (place) =>
                place.place.country && place.place.country.name !== 'any'
            )
            .map((place) => place.place.country.name)
            .flatMap((country) => {
              return r.year.map((year) => {
                record = `resource-${r.id}`
                return {
                  country: country,
                  year: year,
                  id: r.id,
                  type: 'resource',
                  record: record,
                  title: r.title ? r.title[0] : 'No title!',
                  date: r.date_display
                }
              })
            })
        })
      }

      const raw = events.concat(resources).sort((a, b) => {
        const ca = a.country.toLowerCase(),
          cb = b.country.toLowerCase()

        if (ca < cb) {
          return -1
        }
        if (ca > cb) {
          return 1
        }
        return 0
      })
      timeline.raw = raw

      const years = [...new Set(raw.map((d) => d.year))].sort()
      timeline.years = years

      timeline.data = this.prepareTimelineData(raw)

      return timeline
    },
    prepareTimelineData: function (raw) {
      return raw.reduce((acc, curr) => {
        const country = curr.country
        const year = curr.year

        if (!acc[country]) acc[country] = {}
        if (!acc[country][year]) acc[country][year] = []

        acc[country][year].push(curr)

        return acc
      }, {})
    },
    highlight: function (record) {
      if (this.timeline) {
        this.timeline.raw = this.timeline.raw.map((t) =>
          t.record === record ? { ...t, active: true } : { ...t, active: false }
        )
        this.timeline.data = this.prepareTimelineData(this.timeline.raw)
      }
    }
  }
})
