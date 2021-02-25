/* Project specific Javascript goes here. */
$(function () {
  // The ChartDataLabels plugin registers itself globally, meaning that once imported,
  // all charts will display labels. We only need it enabled on specific charts, we
  // need to unregister it globally.
  // https://chartjs-plugin-datalabels.netlify.app/guide/getting-started.html#registration
  Chart.plugins.unregister(ChartDataLabels)

  // override the default image path for leaflet
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

$(function () {
  // Toggle contextual information
  $('.country').on('click', function () {
    $('.info').toggleClass('hidden')

    return false
  })

  // Toggle key
  $('.key-button').on('click', function () {
    $('.key-info').toggleClass('hidden')
    // $('#events-key-svg').attr('viewBox', '0 0 1920 100' ? '0 0 1920 300' : '0 0 1920 100')
    $('#events-key-svg').attr('viewBox', $('#events-key-svg').attr('viewBox') === '0 0 1920 100' ? '0 0 1920 300' : '0 0 1920 100')

    return false
  })

  // Close event info box
  $('.close-event').on('click', function () {
    console.log('Chiudi!')
    alert('Chiudi!')
    return false
  })
})
