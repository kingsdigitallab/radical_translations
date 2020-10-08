new Vue({
  el: '#app',
  delimiters: ['{[', ']}'],
  data: {
    url: new URL(`${window.location}api/`),
    url_suggest: new URL(`${window.location}api/suggest/`),
    query: '',
    query_text: '',
    filters: [],
    ordering: 'title',
    ordering_options: [
      { key: 'title', value: 'title ascending' },
      { key: '-title', value: 'title descending' },
      { key: 'date', value: 'date ascending' },
      { key: '-date', value: 'date descending' }
    ],
    page: 1,
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
          facets.push({
            name: name,
            buckets: this.data.facets[f][name]['buckets']
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
    textSearch: async function (text) {
      this.page = 1
      this.query = this.query_text
      this.query_text = ''

      if (text) {
        this.query = text
      }

      this.data = await this.search()
    },
    search: async function () {
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

      this.url.search = params.toString()
      const response = await fetch(this.url)

      return response.json()
    },
    filterExists: function (filter) {
      return (
        this.filters.find(
          (item) => item[0] === filter[0] && item[1] === filter[1]
        ) !== undefined
      )
    },
    getBucketValue: function (bucket) {
      return bucket.key_as_string ? bucket.key_as_string : bucket.key
    },
    updateFilters: function (filter) {
      if (this.filterExists(filter)) {
        this.filters = this.filters.filter(
          (item) => item[0] !== filter[0] || item[1] !== filter[1]
        )
      } else {
        this.filters.push(filter)
      }
    }
  }
})
