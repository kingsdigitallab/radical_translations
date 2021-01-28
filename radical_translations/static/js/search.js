new Vue({
  el: '#app',
  components: {
    'l-map': window.Vue2Leaflet.LMap,
    'l-marker': window.Vue2Leaflet.LMarker,
    'l-popup': window.Vue2Leaflet.LPopup,
    'l-tile-layer': window.Vue2Leaflet.LTileLayer,
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
    query_dates: [YEAR_MIN, YEAR_MAX],
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
    page_size: PAGE_SIZE !== undefined ? PAGE_SIZE : 50,
    rangeMarks: (v) => v % 10 === 0,
    data: [],
    data_suggest: [],
    map: {
      options: {
        zoomSnap: 0.5
      },
      center: window.L.latLng(53.3439, 0),
      show: false,
      zoom: 4,
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }
  },
  watch: {
    query_text: _.debounce(async function () {
      await this.getSuggestions()
    }, 250),
    page: _.debounce(async function () {
      this.data = await this.search()
    }, 250),
    ordering: async function (newOrdering, oldOrdering) {
      this.data = await this.search()
    },
    filters: async function (newFilters, oldFilters) {
      this.page = 1
      this.data = await this.search()
    },
    'map.show': function (newShow, oldShow) {
      if (newShow) {
        dispatchWindowResizeEvent()
      }
    }
  },
  created: async function () {
    this.loadSearchParams()
    this.data = await this.search()
  },
  computed: {
    facets: function () {
      return this.getFacets().filter(
        (f) => ![...META_FACETS, ...RANGE_FACETS].includes(f.name)
      )
    },
    metaFacets: function () {
      const facets = this.getFacets().filter((f) =>
        META_FACETS.includes(f.name)
      )
      if (facets.length == 1) {
        return facets[0]
      }

      return facets
    },
    rangeFacets: function () {
      const facets = this.getFacets().filter((f) =>
        RANGE_FACETS.includes(f.name)
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

      events = { labels: labels, datasets: [] }

      marker_color = [
                      'rgba(34, 116, 165, 0.4)',
                      'rgba(187, 133, 136, 0.4)',
                      'rgba(84, 13, 110, 0.4)',
                      'rgba(230, 175, 46, 0.4)',
                      'rgba(99, 43, 48, 0.4)',
                      'rgba(11, 3, 45, 0.4)',
                      'rgba(169, 210, 213, 0.4)',
                      'rgba(103, 148, 54, 0.4)'
                      ]

      labels.forEach((label, idx) => {
        let dataset = {
          label: label,
          backgroundColor: marker_color[idx],
          borderColor:marker_color[idx],
          data: []
        }
        this.data.results.forEach((item) => {
          if (item.place.country.name === label) {
            dataset.data.push({
              x: item.year,
              y: idx,
              r: item.related_to.length + 10,
              meta: {
                title: item.title,
                date: item.date,
                place: item.place.address,
                resources: item.related_to.length
              }
            })
          }
        })

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
      this.query_dates = [YEAR_MIN, YEAR_MAX]
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
      let facets = []

      if (this.data.facets !== undefined) {
        Object.keys(this.data.facets).forEach((f) => {
          const name = f.replace('_filter_', '')
          const range = name === 'year' ? true : false
          let buckets = this.data.facets[f][name]['buckets']
          let chartData = {
            labels: [],
            datasets: [
              { label: YEAR_CHART_LABEL, backgroundColor: '#9b2923', data: [] }
            ]
          }

          if (range) {
            //buckets = buckets.flatMap((b) => Array(b.doc_count).fill(b.key))
            buckets.findIndex((b) => b.key === YEAR_MIN) === -1
              ? buckets.unshift({ key: YEAR_MIN, count: 0 })
              : buckets
            buckets.findIndex((b) => b.key === YEAR_MAX) === -1
              ? buckets.push({ key: YEAR_MAX })
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
    },
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
      this.data = await this.search()
    },
    search: async function () {
      const params = new URLSearchParams()

      if (this.query) {
        params.append('search', this.query)
      }

      if (this.query_dates[0] !== YEAR_MIN) {
        params.append('year__gte', this.query_dates[0])
      }
      if (this.query_dates[1] !== YEAR_MAX) {
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

      this.data = await this.search()
    },
    updateFilters: function (filter) {
      if (this.hasFilter(filter)) {
        this.filters = this.filters.filter(
          (item) => item[0] !== filter[0] || item[1] !== filter[1]
        )
      } else {
        this.filters.push(filter)
      }
    }
  }
})
