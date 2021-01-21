new Vue({
  el: '#app',
  components: {
    'l-map': window.Vue2Leaflet.LMap,
    'l-marker': window.Vue2Leaflet.LMarker,
    'l-tile-layer': window.Vue2Leaflet.LTileLayer
  },
  delimiters: ['{[', ']}'],
  data: {
    geo: GEO,
    map: {
      options: {
        zoomSnap: 0.5
      },
      center: GEO,
      zoom: 5,
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }
  },
  mounted: function () {
    setTimeout(function () {
      window.dispatchEvent(new Event('resize'))
    }, 250)
  }
})
