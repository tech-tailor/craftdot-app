// use the service to get the booking details
$(document).ready(function() {
  // Confirm the appliction is loaded, hide loading spinner and unblur
  setTimeout( function() {
    console.log('load')
    $('.container-spinner').hide()
    $('#main-cont, #header-cont').removeClass("blurred");
  })
  console.log('Booking Success Page Loaded')
});