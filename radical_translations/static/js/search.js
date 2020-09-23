new Vue({
  el: '#app',
  delimiters: ['{[', ']}'],
  data: {
    url: new URL(`${window.location}api/`),
    query: '',
    data: [],
    page: 1
  },
  async created() {
    this.data = await this.search()
  },
  methods: {
    async search() {
      if (this.query) {
        this.url.searchParams.append('search', this.query)
      }

      this.url.searchParams.append('page', this.page)
      const response = await fetch(this.url)
      this.url.searchParams.delete('search')
      this.url.searchParams.delete('page')

      return response.json()
    }
  },
  watch: {
    // wait until the user stopped typing before sending the `query`.
    query: _.debounce(async function () {
      this.page = 1
      this.data = await this.search()
    }, 500),
    page: async function () {
      this.data = await this.search()
    }
  }
})
