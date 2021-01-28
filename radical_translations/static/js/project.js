/* Project specific Javascript goes here. */
const dispatchWindowResizeEvent = function () {
  window.dispatchEvent(new Event('resize'))
}

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
        .then((response) => {
          return response.text()
        })
        .then((html) => {
          $(bodyId).html(html)
          $(modalId)
            .modal({ show: true })
            .on('shown.bs.modal', function () {
              dispatchWindowResizeEvent()
            })
        })
    }
  })
})
