new Vue({
  el: '#app',
  delimiters: ['{[', ']}'],
  data: {
    url: new URL(`${window.location}api/`),
    query: '',
    page: 1,
    ordering: 'title',
    ordering_options: [
      { key: 'title', value: 'title ascending' },
      { key: '-title', value: 'title descending' },
      { key: 'date', value: 'date ascending' },
      { key: '-date', value: 'date descending' }
    ],
    filters: [],
    data: []
  },
  async created() {
    this.data = await this.search()
  },
  computed: {
    facets() {
      let facets = []

      if (this.data.facets !== undefined) {
        Object.keys(this.data.facets).forEach((f) => {
          const name = f.replace('_filter_', '')
          facets.push({
            name: name,
            buckets: this.data.facets[f][name]['buckets']
          })
        })
      }

      return facets
    },
    numberOfPages() {
      return Math.ceil(this.data.count / this.data.page_size)
    }
  },
  methods: {
    async search() {
      const params = new URLSearchParams()

      if (this.query) {
        params.append('search', this.query)
      }

      if (!this.page || this.page > this.numberOfPages) {
        this.page = 1
      }

      params.append('page', this.page)
      params.append('ordering', this.ordering)

      this.filters.forEach((filter) =>
        params.append(`${filter[0]}__term`, filter[1])
      )
      console.log(params.toString())

      this.url.search = params.toString()
      const response = await fetch(this.url)

      return response.json()
    },
    filterExists(filter) {
      return (
        this.filters.find(
          (item) => item[0] === filter[0] && item[1] === filter[1]
        ) !== undefined
      )
    },
    updateFilters(filter) {
      if (this.filterExists(filter)) {
        this.filters = this.filters.filter(
          (item) => item[0] !== filter[0] || item[1] !== filter[1]
        )
      } else {
        this.filters.push(filter)
      }
    }
  },
  watch: {
    // wait until the user stopped typing before sending the `query`.
    query: _.debounce(async function () {
      this.page = 1
      this.data = await this.search()
    }, 500),
    page: _.debounce(async function () {
      this.data = await this.search()
    }, 250),
    ordering: async function () {
      this.data = await this.search()
    },
    filters: async function () {
      this.data = await this.search()
    }
  }
})
