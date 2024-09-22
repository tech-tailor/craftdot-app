$( document ).ready(function(e) {




 
  // Submit signup form for processing
  $('#signup').on('click', function(e) {
    e.preventDefault(); 
    let formData = $('#signupForm').serializeArray()

    console.log(formData)


    email = formData[0].value
    password = formData[1].value
    confirm_password = formData[2].value

    emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // validate the forms
  

    
    if ( email === "") {
      $('#messageError').text('Please enter your details').show()
    } else if ( email && !emailRegex.test(email)) {
      $('#messageError').text('Please enter a valid email').show()
    } else if (password === "") {
      $('#messageError').text('Please enter your password').show()
    } else if (password.length < 8 ) {
      $('#messageError').text('Please enter a password of 8 minimum characters').show()
    } else if (confirm_password === "") {
      $('#messageError').text('Please confirm your password').show()
    } else if (password !== confirm_password) {
      $('#messageError').text('Password does not match, retype carefully').show()
    } else {
      registerUser(password, email)
    }

    // Hide error message after 6 secs
    setTimeout(function() {
      $('#messageError').hide()
    }, 6000)

  })

  const registerUser = function(password, email) {
    // Start registration process
    console.log('ajax wan start')
    $.ajax({
      url: '/auth/become-a-craftdotter',
      type: 'POST',
      data: JSON.stringify({
        password: password,
        email: email,
      }),
      contentType: 'application/json',
      dataType: 'json',
      success: function(token) {
        // pop modal to take the otp for verificaton
        $('#otpModal').modal('show')
        // Let the user know otp has been sent
        $('#otpMSG').text('OTP has been sent to you').show()
        // call the function to verify the otp and token
        verifyCode(token)
      },
      error: function( data) {
        $('#messageError').text(data.responseJSON).show()
      }
    })
  }
                                 
    
  

  // submit the otp and token to backend for verification
  const verifyCode = function (token) {
    $('#otpForm').submit(function(e) {
      e.preventDefault();

      let otp = $('#otpInput').val();
      // OTP form validation
      if (otp.length == 0) {
        $('#otpMSG').text('Enter the otp to verify your phone number').show()
      } else if (otp.length < 6) {
        $('#otpMSG').text('Please, enter the complete OTP').show()
      } else if (otp.length > 6) {
        $('#otpMSG').text('Incorrect OTP').show()
      } else {
        // verify the OTP
        $.ajax({
          url: '/auth/verify/otp',
          type: 'POST',
          contentType: 'application/json',
          data: JSON.stringify({
            otp: otp,
            token: token,
          }),
          dataType: 'json',

          // Create user when otp verification succeeds
          success: function(data) {
            // Display OTP response from backend
            $('#otpMSG').text(data).show()
            // Proceed to create user
            createArtisan(token, otp);           
          },

          error: function(data) {
            $('#otpMSG').text(data.responseJSON + ", " + 'try again').show()
            // Reload the web when otp verification failed
            setTimeout(function() {
              window.location.reload()
            }, 6000)
          }
        })
      }
    });
  }
  
  // Create artisan
  
  const createArtisan = function (token, otp) {
    $.ajax({
      url: '/auth/create-artisan',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        otp: otp,
        token: token,
      }),
      dataType: 'json',
      success: function(data) {
        // Redirect to login page 6s after user creation
        $('#otpMSG').text(data).show()
        setTimeout(function() {
          window.location.href = '/auth/login';
        }, 6000)
      },
      error: function(data){
        // Redirect to registration page 2s when an error occured
        $('#otpMSG').text(data.responseJSON).show()
        setTimeout(function() {
          window.location.reload();
        }, 6000)

      }
    })
  }
});
