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
              pointMap('modal-map', place)
            })
        })
    }
  })
})

const project = { maps: {} }

const pointMap = (element, place) => {
  const map = getMap(element)

  map.setView(place, 5)

  L.marker(place).addTo(map)

  map.whenReady(() => map.invalidateSize())
}

const getMap = (element) => {
  if (project.maps[element] !== undefined) {
    project.maps[element].remove()
  }

  const map = L.map(element)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map)

  return (project.maps[element] = map)
}

const dispatchWindowResizeEvent = () => {
  window.dispatchEvent(new Event('resize'))
}



/* UI for static timeline mockup
 * TO DELETE once implemented */

$(function() {
  // Show contextual information
  $('.country').on('click', function () {
    $('.info').toggleClass('hidden');

    return false;
  });
});
