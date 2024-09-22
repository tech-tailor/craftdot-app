// jquery for interaction
$(document).ready(function() {
  // Confirm the appliction is loaded, hide loading spinner and unblur
  setTimeout( function() {
    console.log('load')
    $('.container-spinner').hide()
    $('#main-cont, #header-cont').removeClass("blurred");
  })

});
