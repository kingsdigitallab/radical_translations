new Vue({
  el: '#app',
  components: {
    'l-map': window.Vue2Leaflet.LMap,
    'l-marker': window.Vue2Leaflet.LMarker,
    'l-popup': window.Vue2Leaflet.LPopup,
    'l-tile-layer': window.Vue2Leaflet.LTileLayer,
    'l-marker-cluster': window.Vue2LeafletMarkerCluster,
    'vue-slider': window['vue-slider-component']
  },
  delimiters: ['{[', ']}'],
  data: {
    url: new URL(`${window.location}api/`),
    url_suggest: new URL(`${window.location}api/suggest/`),
    query: '',
    query_text: '',
    query_dates: [1516, 1820],
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
    data: [],
    data_suggest: [],
    map: {
      options: {
        zoomSnap: 0.5
      },
      center: window.L.latLng(53.3439, 0),
      show: true,
      zoom: 3,
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }
  },
  watch: {
    query_dates: _.debounce(async function () {
      this.data = await this.search()
    }, 250),
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
      this.data = await this.search()
    }
  },
  created: async function () {
    this.data = await this.search()
  },
  computed: {
    facets: function () {
      let facets = []

      if (this.data.facets !== undefined) {
        Object.keys(this.data.facets).forEach((f) => {
          const name = f.replace('_filter_', '')
          const range = name === 'year' ? true : false
          let buckets = this.data.facets[f][name]['buckets']
          let max,
            min = 0

          if (range) {
            //buckets = buckets.flatMap((b) => Array(b.doc_count).fill(b.key))
            buckets = buckets.map((b) => b.key)
            max = Math.max(buckets)
            min = Math.min(buckets)
          }

          facets.push({
            name: name,
            range: range,
            buckets: buckets,
            min: min,
            max: max
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
    }
  },
  methods: {
    getFacetDisplayName: function (name) {
      return name.replaceAll('_', ' ')
    },
    clearFilters: function () {
      this.filters = []
      this.query = ''
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
    search: async function () {
      const params = new URLSearchParams()

      if (this.query) {
        params.append('search', this.query)
      }

      params.append('year__gte', this.query_dates[0])
      params.append('year__lte', this.query_dates[1])

      if (!this.page || this.page > this.numberOfPages) {
        this.page = 1
      }

      params.append('page', this.page)

      if (this.ordering !== this.ordering_default) {
        params.append('ordering', this.ordering)
      }

      this.filters.forEach((filter) =>
        params.append(`${filter[0]}__term`, filter[1])
      )

      this.url.search = params.toString()
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
