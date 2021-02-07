/* Project specific Javascript goes here. */
$(function () {
  L.Icon.Default.imagePath = '/static/leaflet/dist/images/'

  // highlight active tab and allow permalink for bibliography and record pages
  const hash = window.location.hash

  if (hash) {
    $(`.nav[role="tablist"] a[href="${hash}"]`).tab('show')
  }

  $('a[role="tab"]').on('click', function () {
    const hash = $(this).attr('href')
    const url = `${window.location.origin}${window.location.pathname}${hash}`

    history.replaceState(null, null, url)
  })

  // enable tooltips
  $('[data-toggle="tooltip"]').tooltip()

  // modals
  $('.modal-toggle').on('click', function () {
    const url = $(this).data('href')

    if (url) {
      const modalId = '#place-modal'
      const bodyId = `${modalId} .modal-body`

      fetch(url)
        .then((response) => response.json())
        .then((place) => {
          $(modalId)
            .modal({ show: true })
            .on('shown.bs.modal', function () {
              $(`${bodyId} h2`).html(`${place.address}, ${place.country.name}`)
              pointMap(place)
            })
        })
    }
  })
})

const pointMap = (point) => {
  const map = L.map('modal-map').setView(point, 5)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map)

  L.marker(point).addTo(map)

  map.whenReady(() => map.invalidateSize())
}

const dispatchWindowResizeEvent = () => {
  window.dispatchEvent(new Event('resize'))
}
