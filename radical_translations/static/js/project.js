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

  // Commenting cookie disclaimer.
  // Re-enable if we start using cookies.

  // if (!Cookies.get('radical-translations-cookie')) {
  //     $("#cookie-disclaimer").removeClass('hidden');
  // }
  // // Set cookie and hide the box
  // $('#cookie-disclaimer .btn-success').on("click", function() {
  //     Cookies.set('radical-translations-cookie', 'radical-translations-cookie-set', { expires: 30 });
  //     $("#cookie-disclaimer").addClass('hidden');
  // });
  // // Hide the box don't set the cookie
  // $('#cookie-disclaimer .close').on("click", function() {
  //     $("#cookie-disclaimer").addClass('hidden');
  // });
})
