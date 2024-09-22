$( document ).ready(function() {
  // Confirm the appliction is loaded, hide loading spinner and unblur
  setTimeout( function() {
    $('.container-spinner').hide()
    $('#main-cont, #header-cont').removeClass("blurred");
  })

  /* Profile select input tab */
  $('#accountState').change(function() {
    var selectedValue = $(this).val();
    switch (selectedValue) {
      case 'profile':
        window.location.href = '/account/profile';
        break;
      case 'password':
        window.location.href = '/account/password';
        break;
      case 'notification':
        window.location.href = '/account/notification';
        break;
      case 'my-task':
        window.location.href = '/account/my-tasks';
        break;
      default:
        window.location.href = '/account/profile';
        // Optional: Handle unexpected values
        break;
    }
  });

  // Get all the user data
  const user_data = JSON.parse($('#theUserData').html())

  // fill each field of the user profile
  $('#userNames').text(user_data.first_name + " " + user_data.last_name)
  $('#userPhone').text(user_data.phone_number)
  $('#userEmail').text(user_data.email)

  if (user_data.role == 'artisan') {
    $('#userType').text('Artisan account')
  } else if (user_data.role == 'user'){
    $('#userType').text('Client account')
  }
  
  // Update user details when edit button is clicked
  $('#editProfile').click(function() {
    const user = JSON.parse($('#theUserData').html())
    const artisan = JSON.parse($('#theArtisanData').html())

    // Update the profile picture 
    $('#profilePicture').on('click', function() {
      $('#inputPicture').click();
    });
    $('#inputPicture').on('change', function(e) {
      const file = e.target.files[0]
      if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
          $('#profilePicture').attr('src', e.target.result);
        };
        reader.readAsDataURL(file);
      }
    });

    console.log('about to serve image')
    console.log(artisan)
    // Servr the profile picture
    $.ajax({
      url: '/account/serve_image',
      method: 'GET',
      success: function(image_url) {
          if (image_url) {
            console.log('imageurl........', image_url)
            // Set the src attribute of the img tag
            $('#profilePicture').attr('src', image_url);
            console.log('Image loaded');
          } else {
            console.log('Image not found');
          }
      },
      error: function(error) {
          //alert('Error retrieving image');
          console.log('error', error)
      }
    });


    const updateArtisan = function(){
      // dynamically arrange the the template for account update
      $('#accountDetails').hide();
      $('#subtitle').text('Account Update');
      $('#editProfile').hide();
      $('#userForm').show();
      // Prefill the fields with the user data when edit is clicked
      $('#profilePicture').attr('src', `/uploads/${user.id}/${user.profile_picture}`)
      //console.log('profile picture', `/uploads/${user.id}/${user.profile_picture}`)
      $('#phoneNumber').val(user.phone_number)
      $('#firstName').val(user.first_name)
      $('#lastName').val(user.last_name)
      $('#email').val(user.email)
      $('#phoneNumber').val(user.phone_number)
      $('#streetAddress').val(user.street_address)
      $('#state').val(user.state)
      $('#country').val(user.country)
      //$('#service').val(artisan.service)
      console.log('user', user)
    }

    const updateUser = function() {
      // dynamically arrange the the template for account update
      $('#accountDetails').hide();
      $('#subtitle').text('Account Update');
      $('#editProfile').hide();
      $('#userForm').show();
      $('.service-type').hide();
      // Update the fields with the user data
      $('#profilePicture').attr('src', user.profile_picture)
      $('#phoneNumber').val(user.phone_number)
      $('#firstName').val(user.first_name)
      $('#lastName').val(user.last_name)
      $('#email').val(user.email)
      $('#phoneNumber').val(user.phone_number)
      $('#streetAddress').val(user.street_address)
      $('#myLGA').val(user.lga)
      $('#state').val(user.state)
      $('#country').val(user.country)
    }


    if (user_data.role == 'user') {
      updateUser()
    } else if (user_data.role == 'artisan') {
      //update user and show some fields belonging to artisans
      updateArtisan()
    }

    // Secure the some profile details from editing
    const email = $('#email').val()
    const first_name = $('#firstName').val()
    const last_name = $('#lastName').val()
    const country = $('#country').val()
    const phone_number = $('#phoneNumber').val()
    console.log(email, first_name, last_name, country)
    if (email) {
      $('#email').on('focus', function() {
        this.blur();
      });
    }
    if (first_name) {
      $('#firstName').on('focus', function() {
        this.blur();
      });
    }
    if (last_name) {
      $('#lastName').on('focus', function() {
        this.blur();
      });
    }
    if (country) {
      $('#country').on('focus', function() {
        this.blur();
      }); 
    }

    if (phone_number) {
      $('#phoneNumber').on('focus', function() {
        this.blur();
      }); 
    }
    
    
    
    

    // Cancel button
    $('#cancel').click( function() {
      window.location.href = '/account/profile';
    })
    // save/update the new user details
    $('#userUpdateform').on('submit', function(e) {
      e.preventDefault()
      formData = new FormData(this)
      for (let pair of formData.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
      }

      // Send the data to the 
      $.ajax({
        type: "PUT",
        url: "/account/profile",
        data: formData,
        contentType: false,
        processData: false,
        success: function(data) {
          if (data.status_code === 200) {
            console.log('Profile updated successfully')
            // Redirect to the profile page
            //window.location.href = '/account/profile'
          } else {
            console.log(data)
          }
        },
        error: function(jqXHR, textStatus, errorThrown) {
          console.error('Error submitting form:', textStatus, errorThrown);
          // Handle error response
        }
      })
    });
  });
 

});



