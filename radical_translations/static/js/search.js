const YEAR_MIN = 1516
const YEAR_MAX = 1820

Vue.component('bar-chart', {
  extends: VueChartJs.Bar,
  props: ['clickHandler'],
  mixins: [VueChartJs.mixins.reactiveProp],
  mounted() {
    const self = this
    this.renderChart(this.chartData, {
      legend: { display: false },
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true
            }
          }
        ]
      },
      onClick: function (evt, item) {
        if (item.length > 0) {
          const year = item[0]['_model'].label
          self.clickHandler(year, year)
        }
      }
    })
  }
})

new Vue({
  el: '#app',
  components: {
    'vue-slider': window['vue-slider-component']
  },
  delimiters: ['{[', ']}'],
  data: {
    url: new URL(`${window.location}api/`),
    url_suggest: new URL(`${window.location}api/suggest/`),
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
    rangeMarks: (v) => v % 10 === 0,
    data: [],
    data_suggest: []
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
          let chartData = {
            labels: [],
            datasets: [{ label: name, backgroundColor: '#9b2923', data: [] }]
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
    rangeSearch: async function () {
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
