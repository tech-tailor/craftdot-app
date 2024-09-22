$( document ).ready(function() {

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

  
});



