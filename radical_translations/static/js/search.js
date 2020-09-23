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
    data: []
  },
  async created() {
    this.data = await this.search()
  },
  computed: {
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

      this.url.search = params.toString()
      const response = await fetch(this.url)

      return response.json()
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
    }
  }
})
