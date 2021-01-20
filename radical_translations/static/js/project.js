/* Project specific Javascript goes here. */

$(function () {
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
      const modalId = $(this).data('target')
      const bodyId = `${modalId} .modal-body`

      if (!$.trim($(bodyId).html())) {
        $(bodyId).load(url, function () {})
      }
      $(modalId).modal({ show: true })
    }
  })
})
