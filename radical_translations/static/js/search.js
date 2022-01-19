let baseURL = `${window.location.origin}${window.location.pathname}`;
if (window.viewBaseURL) {
  baseURL = viewBaseURL;
}

Vue.use(VueHtmlToPaper, {
  styles: ["/static/css/project.min.css"],
});

new Vue({
  el: "#app",
  components: {
    "vue-slider": window["vue-slider-component"],
  },
  delimiters: ["{[", "]}"],
  data: {
    url: new URL(`${baseURL}api/`),
    urlResources: new URL(`${baseURL}../resources/api-simple/`),
    urlSuggest: new URL(`${baseURL}api/suggest/`),
    query: "",
    query_text: "",
    query_dates: [options.year_min, options.year_max],
    has_date_query: false,
    filters: [],
    ordering_default: "score",
    ordering: "score",
    ordering_options: options.ordering,
    page: 1,
    page_size: options.page_size !== undefined ? options.page_size : 50,
    rangeMarks: (v) => v % 10 === 0,
    data: [],
    data_suggest: [],
    map: {
      mapObject: null,
      options: {
        zoomSnap: 0.5,
      },
      center: window.L.latLng(53.3439, 0),
      show: false,
      zoom: 4,
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      popup: {
        item: null,
        place: null,
      },
    },
    resources: {},
    timeline: { filters: {} },
    timelineDetail: { country: null, year: null, data: [], show: false },
    zoom: "",
    zoomLevels: [
      { level: "Small", style: "zsmall" },
      { level: "Medium", style: "" },
      { level: "Large", style: "zlarge" },
    ],
  },
  watch: {
    query_text: _.debounce(async function () {
      await this.getSuggestions();
    }, 250),
    page: _.debounce(async function () {
      await this.search();
    }, 250),
    ordering: async function (newOrdering, oldOrdering) {
      await this.search();
    },
    filters: async function (newFilters, oldFilters) {
      this.page = 1;
      await this.search();
    },
    "map.show": async function (newShow, oldShow) {
      if (newShow) {
        this.page = 1;
        this.page_size = 2000;
        dispatchWindowResizeEvent();
      } else {
        this.page_size = options.page_size;
      }

      await this.search();
    },
  },
  created: async function () {
    this.loadSearchParams();

    await this.search();

    this.getMap();

    this.focusTimeline();
  },
  computed: {
    facets: function () {
      return this.getFacets().filter(
        (f) =>
          ![...options.meta_facets, ...options.range_facets].includes(f.name)
      );
    },
    metaFacets: function () {
      const facets = this.getFacets().filter((f) =>
        options.meta_facets.includes(f.name)
      );
      if (facets.length == 1) {
        return facets[0];
      }

      return facets;
    },
    rangeFacets: function () {
      const facets = this.getFacets().filter((f) =>
        options.range_facets.includes(f.name)
      );

      return facets;
    },
    numberOfPages: function () {
      return Math.ceil(this.data.count / this.data.page_size);
    },
    suggestions: function () {
      let suggestions = [];

      if (this.data_suggest !== undefined) {
        Object.keys(this.data_suggest).forEach((s) => {
          this.data_suggest[s][0].options.forEach((o) =>
            suggestions.push(o.text)
          );
        });
      }

      return suggestions;
    },
  },
  methods: {
    getFacetDisplayName: function (name) {
      return name.replace(/_/g, " ");
    },
    clearFilters: function () {
      this.filters = [];
      this.page = 1;
      this.query = "";
      this.query_dates = [options.year_min, options.year_max];
    },
    getBucketValue: function (bucket) {
      return bucket.key_as_string ? bucket.key_as_string : bucket.key;
    },
    getContributions: function (item) {
      return item.contributions
        .filter((c) => c.agent.name !== "any")
        .map((c) => ({
          agent: c.agent,
          roles: c.roles.filter((r) => r.label !== undefined),
        }));
    },
    getFacets: function () {
      return this.getFacetsCache(this.data);
    },
    getFacetsCache: _.memoize(function (data) {
      let facets = [];

      if (data.facets !== undefined) {
        Object.keys(data.facets).forEach((f) => {
          const name = f.replace("_filter_", "");
          const range = name === "year" ? true : false;
          let buckets = data.facets[f][name]["buckets"];
          let chartData = {
            labels: [],
            datasets: [
              { label: options.label, backgroundColor: "#9b2923", data: [] },
            ],
          };

          if (range) {
            //buckets = buckets.flatMap((b) => Array(b.doc_count).fill(b.key))
            buckets.findIndex((b) => b.key === options.year_min) === -1
              ? buckets.unshift({ key: options.year_min, count: 0 })
              : buckets;
            buckets.findIndex((b) => b.key === options.year_max) === -1
              ? buckets.push({ key: options.year_max })
              : buckets;
            chartData.labels = buckets.map((b) => b.key);
            chartData.datasets[0].data = buckets.map((b) => b.doc_count);
          }

          facets.push({
            name: name,
            range: range,
            buckets: buckets,
            chartData: chartData,
            display: this.query_dates,
          });
        });
      }

      facets.sort(function (a, b) {
        const nameA = a.name.toUpperCase();
        const nameB = b.name.toUpperCase();

        if (nameA < nameB) {
          return -1;
        }
        if (nameA > nameB) {
          return 1;
        }

        return 0;
      });

      return facets;
    }),
    getFacetCount: function (buckets) {
      return buckets
        .map((el) => el.doc_count)
        .reduce((acc, cur) => Math.max(acc, cur), 0);
    },
    getSuggestions: async function () {
      if (!this.query_text) {
        this.data_suggest = [];
        return;
      }

      const params = new URLSearchParams();
      params.append("suggest_field", this.query_text);

      this.urlSuggest.search = params.toString();
      this.data_suggest = await fetch(this.urlSuggest).then((response) =>
        response.json()
      );
    },
    handleChartClick: async function (from, to) {
      this.query_dates = [from, to];
      await this.rangeSearch();
    },
    hasAny: function (facet) {
      return facet.buckets.find((b) => this.getBucketValue(b) === "any");
    },
    hasFilter: function (filter) {
      return (
        this.filters.find(
          (item) =>
            item[0] === filter[0] &&
            (filter[1] === undefined || item[1] === filter[1])
        ) !== undefined
      );
    },
    loadSearchParams: function () {
      const params = new URLSearchParams(window.location.search);

      let key = "page";
      if (params.has(key)) {
        this.page = params.get(key);
        params.delete(key);
      }

      key = "page_size";
      if (params.has(key)) {
        this.page_size = params.get(key);
        params.delete(key);
      }

      key = "search";
      if (params.has(key)) {
        this.query = params.get(key);
        params.delete(key);
      }

      key = "year__gte";
      if (params.has(key)) {
        this.query_dates[0] = params.get(key);
        params.delete(key);
      }

      key = "year__lte";
      if (params.has(key)) {
        this.query_dates[1] = params.get(key);
        params.delete(key);
      }

      for (const key of params.keys()) {
        this.updateFilters([key.replace("__term", ""), params.get(key)]);
      }
    },
    rangeSearch: async function (reset = false) {
      this.page = 1;
      if (reset === true) {
        this.query_dates = [options.year_min, options.year_max];
      }
      await this.search();
    },
    search: async function () {
      this.data = await this.doSearch();

      if (options.resources) {
        this.resources = await this.doSearch(
          this.urlResources,
          1000,
          this.query_dates[0],
          this.query_dates[1],
          true
        );
        this.timeline = this.getTimeline();
      }
      if (this.map.show) {
        this.renderMap();
      }
    },
    doSearch: async function (
      url = this.url,
      page_size = this.page_size,
      year_from = this.query_dates[0],
      year_to = this.query_dates[1],
      all = false
    ) {
      const params = new URLSearchParams();

      if (this.query) {
        params.append("search", this.query);
      }

      if (year_from !== options.year_min) {
        params.append("year__gte", year_from);
      }
      if (year_to !== options.year_max) {
        params.append("year__lte", year_to);
      }

      if (params.has("year__gte") || params.has("year__lte")) {
        this.has_date_query = true;
      } else {
        this.has_date_query = false;
      }

      if (!this.page || this.page > this.numberOfPages) {
        this.page = 1;
      }

      params.append("page", this.page);
      params.append("page_size", page_size);

      if (this.ordering !== this.ordering_default) {
        params.append("ordering", this.ordering);
      }

      this.filters.forEach((filter) =>
        params.append(`${filter[0]}__term`, filter[1])
      );

      url.search = params.toString();
      window.history.pushState({}, "", url.search);

      let json = {};
      do {
        let response = await fetch(url);
        _.mergeWith(json, await response.json(), (objValue, srcValue) =>
          _.isArray(objValue) ? objValue.concat(srcValue) : srcValue
        );

        url = json.next;
      } while (url && all);

      return json;
    },
    textSearch: async function (text) {
      this.page = 1;
      this.query = this.query_text;
      this.query_text = "";

      if (text) {
        this.query = text;
      }

      await this.search();
    },
    updateFilters: function (filter) {
      if (this.hasFilter(filter)) {
        this.filters = this.filters.filter(
          (item) => item[0] !== filter[0] || item[1] !== filter[1]
        );
      } else {
        this.filters.push(filter);
      }
    },
    getMap: function () {
      if (!document.getElementById("map")) return;

      if (this.map.mapObject) this.map.mapObject.remove();

      const map = L.map("map");
      map.setView(this.map.center, this.map.zoom);

      L.tileLayer(this.map.url, {
        attribution: this.map.attribution,
      }).addTo(map);

      this.map.mapObject = map;

      return this.map.mapObject;
    },
    renderMap: function () {
      const map = this.getMap();
      if (!map) return;

      const cluster = L.markerClusterGroup();

      const vue = this;
      this.data.results.forEach((item) =>
        item[options.map_field].forEach((p) => {
          const place = p.place !== undefined ? p.place : p;

          if (place !== undefined && place.geo !== undefined) {
            cluster.addLayer(
              L.marker(place.geo).on("click", function () {
                const marker = this;

                vue.map.popup.item = item;
                vue.map.popup.place = place;

                vue.$nextTick(() =>
                  marker
                    .bindPopup(
                      document.getElementById("map-popup-container").innerHTML
                    )
                    .openPopup()
                );
              })
            );
          }
        })
      );

      map.addLayer(cluster);

      map.whenReady(() => map.invalidateSize());
    },
    getTimeline: function () {
      const timeline = { filters: {} };

      if (!this.data || !this.data.results) {
        return timeline;
      }

      const events = this.data.results.flatMap((r) => {
        return r.country.flatMap((country, idx) => {
          return !r.year
            ? []
            : r.year.map((year) => {
                const record = `event-${r.id}`;
                const uid = `${record}-${country}-${year}`;

                const classification = r.classification
                  .filter((c) => c !== "any")
                  .flatMap((c) => c);

                let relatedTags = [];
                if (idx > 0) {
                  relatedTags = ["related", this.timelineFacet(r.country[0])];
                }

                return {
                  country: country,
                  year: year,
                  id: r.id,
                  type: "event",
                  subtype: "event",
                  record: record,
                  title: r.title,
                  date: r.date,
                  subjects: classification,
                  tags: [this.timelineFacet(country)]
                    .concat(relatedTags)
                    .concat(classification.map((c) => this.timelineFacet(c))),
                };
              });
        });
      });

      let resources = [];

      if (this.resources && this.resources.results) {
        resources = this.resources.results
          .filter(
            (r) =>
              r.form_genre.filter(
                (fr) =>
                  fr.label === "Serial publications" ||
                  fr.label === "Periodicals"
              ).length === 0
          )
          .filter((r) => r.is_original || r.is_translation)
          .flatMap((r) => {
            return r.places
              .filter(
                (place) =>
                  place.place.country && place.place.country.name !== "any"
              )
              .map((place) => place.place.country.name)
              .flatMap((country) => {
                const subjects = r.form_genre
                  .filter((fr) => fr.label !== "any")
                  .map((fr) => fr.label);

                return !r.year
                  ? []
                  : r.year.map((year) => {
                      const record = `resource-${r.id}`;
                      const uid = `${record}-${country}-${year}`;

                      return {
                        country: country,
                        year: year,
                        id: r.id,
                        type: "resource",
                        subtype: r.is_original ? "source text" : "translation",
                        record: record,
                        title: r.title ? r.title[0] : "No title!",
                        date: r.date_display,
                        subjects: subjects,
                        tags: [
                          this.timelineFacet(country),
                          r.is_original ? "source-text" : "translation",
                        ],
                      };
                    });
              });
          });
      }

      const raw = events.concat(resources).sort((a, b) => {
        const ca = a.country.toLowerCase(),
          cb = b.country.toLowerCase();

        if (ca < cb) {
          return -1;
        }
        if (ca > cb) {
          return 1;
        }
        return 0;
      });
      timeline.raw = raw;

      const years = [...new Set(raw.map((d) => d.year))].sort();
      timeline.years = years;

      timeline.data = this.prepareTimelineData(raw);

      return timeline;
    },
    timelineFacet: function (text) {
      return text.toLowerCase().replace(" ", "-");
    },
    prepareTimelineData: function (raw) {
      const other = "Other";
      const data = {
        France: {},
        Ireland: {},
        Italy: {},
        "United Kingdom": {},
        "United States": {},
        Other: {},
      };

      return raw.reduce((acc, curr) => {
        let country = curr.country;
        const year = curr.year;

        if (!(country in acc)) {
          country = other;
        }

        if (acc[country]["filtered"] === undefined)
          acc[country]["filtered"] = true;
        acc[country]["filtered"] = acc[country]["filtered"] && curr.filtered;

        if (!acc[country][year]) acc[country][year] = [];
        acc[country][year].push(curr);

        return acc;
      }, data);
    },
    highlight: function (record) {
      if (this.timeline) {
        this.timeline.raw = this.timeline.raw.map((t) =>
          t.record === record ? { ...t, active: true } : { ...t, active: false }
        );
        this.timeline.data = this.prepareTimelineData(this.timeline.raw);
      }
    },
    getTimelineDetail: function (country, year, record) {
      this.timelineDetail.country = country;
      this.timelineDetail.year = year;
      this.timelineDetail.data = this.timeline.data[country][year];

      if (record) {
        this.timelineDetail.record = this.timelineDetail.data.filter(
          (d) => d.record === record
        )[0];
      }

      this.timelineDetail.show = true;
    },
    setZoom: function (value) {
      this.zoom = value;

      this.focusTimeline(true);
      this.$nextTick(() => {
        this.focusTimeline(false);
      });
    },
    focusTimeline: function (reset = false) {
      const el = document.getElementById("timeline-table");

      if (el === null || el === undefined) return;

      if (reset) {
        el.scrollLeft = 0;
      } else {
        const w = el.scrollWidth;
        el.scrollLeft = w / 2 + w / 8;
      }
    },
    filterTimeline: function (facet, value) {
      if (this.timeline) {
        const current = this.timeline.filters[facet];

        if (current === value) {
          delete this.timeline.filters[facet];
        } else {
          this.timeline.filters[facet] = value;
        }

        const values = Object.values(this.timeline.filters);

        if (values.length > 0) {
          this.timeline.raw = this.timeline.raw.map((t) =>
            values.every((v) => t.tags.includes(v))
              ? { ...t, filtered: false }
              : { ...t, filtered: true }
          );
        } else {
          this.timeline.raw = this.timeline.raw.map((t) => {
            return { ...t, filtered: false };
          });
        }

        this.timeline.data = this.prepareTimelineData(this.timeline.raw);
      }
    },
    print: async function (element) {
      this.$htmlToPaper(element);
    },
  },
});
