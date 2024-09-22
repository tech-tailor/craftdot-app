$( document ).ready( function() {

	// Toggle the email/phone input
  // Hide Phone number input
  $('#phoneSignin').hide()

  // Hide and clear email input when phone input
  $('#phoneToggle').on('click', function(e) {
    e.preventDefault();
    $('#email').val("");
    $('#phoneSignin').show();
    $('#emailSignin').hide();
  });

  // Hide and clear phone input when email input
  $('#emailToggle').on('click', function(e) {
    e.preventDefault();
    $('#emailSignin').show();
    $('#phoneNumber').val("");
    $('#phoneSignin').hide();
  });
    

});