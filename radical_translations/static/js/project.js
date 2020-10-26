/* Project specific Javascript goes here. */

// Highlight active tab and allow permalink for bibliography and record pages
$(function () {
  const hash = window.location.hash

  if (hash) {
    $(`.nav[role="tablist"] a[href="${hash}"]`).tab('show')
  }

  $('a[role="tab"]').on('click', function () {
    const hash = $(this).attr('href')
    const url = `${window.location.origin}${window.location.pathname}${hash}`

    history.replaceState(null, null, url)
  })
})

// Set cookies and display cookies disclaimer
$(document).ready(function() {
    if (!Cookies.get('ctrs-cookie')) {
        $("#cookie-disclaimer").removeClass('hidden');
    }
    // Set cookie and hide the box
    $('#cookie-disclaimer .success').on("click", function() {
        Cookies.set('ctrs-cookie', 'ctrs-cookie-set', { expires: 30 });
        $("#cookie-disclaimer").addClass('hidden');
    });
    // Hide the box don't set the cookie
    $('#cookie-disclaimer .close').on("click", function() {
        $("#cookie-disclaimer").addClass('hidden');
    });
});