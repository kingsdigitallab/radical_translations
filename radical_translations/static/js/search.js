new Vue({
  el: '#app',
  components: {
    'vue-slider': window['vue-slider-component']
  },
  delimiters: ['{[', ']}'],
  data: {
    url: new URL(`${window.location.origin}${window.location.pathname}api/`),
    url_suggest: new URL(
      `${window.location.origin}${window.location.pathname}api/suggest/`
    ),
    query: '',
    query_text: '',
    query_dates: [options.year_min, options.year_max],
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
    events: { country: null, year: null, data: [] }
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
        this.page_size = 1000
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
      labels.forEach((label, idx) => {
        const colour = colours[label]

        let dataset = {
          label: label,
          backgroundColor: colour,
          borderColor: colour,
          data: []
        }

        this.data.results.forEach((item) => {
          // for each event in the country
          if (item.place.country.name === label && item.year) {
            item.year.forEach((year) => {
              dataset.data.push({
                x: year,
                y: idx,
                r: 5,
                meta: {
                  id: item.id,
                  year: year,
                  place: item.place.address,
                  n: 1,
                  resources: item.related_to.length
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

      this.url_suggest.search = params.toString()
      this.data_suggest = await fetch(this.url_suggest).then((response) =>
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
    rangeSearch: async function () {
      this.page = 1
      await this.search()
    },
    search: async function () {
      this.data = await this.doSearch()
      if (this.map.show) {
        this.renderMap()
      }
    },
    doSearch: async function () {
      const params = new URLSearchParams()

      if (this.query) {
        params.append('search', this.query)
      }

      if (this.query_dates[0] !== options.year_min) {
        params.append('year__gte', this.query_dates[0])
      }
      if (this.query_dates[1] !== options.year_max) {
        params.append('year__lte', this.query_dates[1])
      }

      if (!this.page || this.page > this.numberOfPages) {
        this.page = 1
      }

      params.append('page', this.page)
      params.append('page_size', this.page_size)

      if (this.ordering !== this.ordering_default) {
        params.append('ordering', this.ordering)
      }

      this.filters.forEach((filter) =>
        params.append(`${filter[0]}__term`, filter[1])
      )

      this.url.search = params.toString()
      window.history.pushState({}, '', this.url.search)

      const response = await fetch(this.url)

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
        item.places.forEach((place) => {
          if (place.place.geo !== undefined) {
            cluster.addLayer(
              L.marker(place.place.geo).on('click', function () {
                const marker = this

                vue.map.popup.item = item
                vue.map.popup.place = place.place

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

      const url = this.url
      url.search = params.toString()

      const data = fetch(url)
        .then((response) => response.json())
        .then((data) => {
          this.events.data = data.results
        })
    }
  }
})
