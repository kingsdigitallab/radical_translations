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
      show: false,
      zoom: 3,
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }
  }
})
