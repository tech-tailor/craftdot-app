$( document ).ready(function(e) {


  
  // Toggle the email/phone input
  // Hide Phone number input
  $('#phoneSignup').hide()

  // Hide and clear email input when phone input
  $('#phoneToggle').on('click', function(e) {
    e.preventDefault();
    $('#email').val("");
    $('#phoneSignup').show();
    $('#emailSignup').hide();
  });

  // Hide and clear phone input when email input
  $('#emailToggle').on('click', function(e) {
    e.preventDefault();
    $('#phoneNumber').val("");
    $('#emailSignup').show();
    $('#phoneSignup').hide();
  });

 
  // Submit signup form for processing
  $('#signup').on('click', function(e) {
    e.preventDefault(); 
    let formData = $('#signupForm').serializeArray()


    email = formData[1].value
    phone_number = formData[0].value
    password = formData[2].value
    confirm_password = formData[3].value
    
    phoneNumberRegex = /^\d*$/;
    emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // validate the forms
    if (phone_number && email === "") {
      if (!phoneNumberRegex.test(phone_number)) {
        $('#messageError').text('Please enter a valid phone number').show()
      } else if (phone_number.length < 11) {
        $('#messageError').text('Please enter a complete phone number').show()
      } else if (password === "") {
        $('#messageError').text('Please enter your password').show()
      } else if (password.length < 8 ) {
        $('#messageError').text('Please enter a password of 8 minimum characters').show()
      } else if (confirm_password === "") {
        $('#messageError').text('Please confirm your password').show()
      } else if (password !== confirm_password) {
        $('#messageError').text('Password does not match, retype carefully').show()
      } else {
        registerUser(phone_number, password, email)
      }

    } else if (email && phone_number === "") {
      if (!emailRegex.test(email)) {
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
        registerUser(phone_number, password, email)
      }
    } else if (phone_number === "" && email == "") {
      $('#messageError').text('Please enter your details').show()
    }

    // Hide error message after 6 secs
    setTimeout(function() {
      $('#messageError').hide()
    }, 6000)

  })

  const registerUser = function(phone_number, password, email) {
    // Start registration process
    console.log('ajax wan start')
    $.ajax({
      url: '/auth/register',
      type: 'POST',
      data: JSON.stringify({
        phone_number: phone_number,
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
            createUser(token, otp);           
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
  
  // Create user 
  
  const createUser = function (token, otp) {
    $.ajax({
      url: '/auth/create-user',
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
