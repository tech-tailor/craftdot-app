$( document ).ready(function() {
	// Confirm the appliction is loaded, hide loading spinner and unblur
  setTimeout( function() {
    console.log('load')
    $('.container-spinner').hide()
    $('#main-cont, #header-cont').removeClass("blurred");
  })
	
	// Timeout settings for flash message
	$('#flashMessage').each(function(index, element) {
		setTimeout(() => {
				$(element).fadeOut('slow');
		}, 7000 * (index + 1)); // flash message to dissapear in 5sec
	
	})

});
