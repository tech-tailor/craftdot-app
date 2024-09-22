$( document ).ready(function() {
  console.log('startaa')
  $('#userUpdateform').on('submit', function(e) {
    e.preventDefault()
    // Get the form data
    formData = new FormData(this)
    for (let pair of formData.entries()) {
      console.log(pair[0] + ': ' + pair[1]);
    }

    // Send the data to the
    $.ajax({
      type: 'PUT',
      url: '/account/update_name',
      data: formData,
      contentType: false,
      processData: false,
      success: function(response) {
        console.log('response', response)
        // Redirect to the profile page
        window.location.href = '/services/booking'
      },
      error: function(error) {
        console.log('error', error)
        
      }
    })
  })

  // Cancel button
  $('#cancel').click( function() {
    window.location.href = '/';
  })

});



