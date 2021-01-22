$(function () {
  L.Icon.Default.imagePath = '/static/leaflet/dist/images/'
  const map = L.map('map').setView(GEO, 5)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map)

  L.marker(GEO).addTo(map)

  map.whenReady(function () {
    setTimeout(() => {
      map.invalidateSize()
    }, 250)
  })
})
