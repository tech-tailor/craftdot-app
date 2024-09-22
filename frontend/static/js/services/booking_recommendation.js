// use the service to get the booking details
$(document).ready(function() {
  //  Confirm the appliction is loaded, hide loading spinner and unblur
  setTimeout( function() {
    $('.container-spinner').hide()
    $('#main-cont, #header-cont').removeClass("blurred");

  })
  // Extract data from the embedded JSON
  const artisans = JSON.parse($('#dataForArtisans').html());
  const artisansUserData = JSON.parse($('#dataForArtisansUser').html());
  const serviceType = JSON.parse($('#serviceType').html());
  // Dynamically update the available artisans
  const availableArtisans = function ()  {
    artisans.forEach((artisan, index) => {
      artisansUserData.forEach((userData, index) => {
        if (artisan.user_id == userData.id) {
          // Create the artisan board
          $('#crafter-boards').append(createArtisanBoard(artisan, userData));
          // Send these details to html for further
          $( '#artisanProfilepicture').val(userData.profile_picture)
          $('#artisanName').val(userData.first_name)
          $('#serviceName').val(serviceType)
          $('#artisanPrice').val(artisan.pricing)
          $('#artisanID').val(artisan.id)
          console.log('Pricing......', artisan.pricing)
          
        } 
      })
    })
  }
  availableArtisans()

  // Create artisan board
  function createArtisanBoard(artisan, artisanData) {
    return `
      <div class="artisan-board">
        <div class="artisan-card">
          <img class="user-picture" src="${artisanData.profile_picture}" alt="${artisanData.first_name}">
          <p class="name">${artisanData.first_name}</p>
          <p class="price">#${artisan.pricing}/hr</p>
          <p class="reviews"> 4.8 (10 reviews)</p>
          <p class="service"> 300 ${serviceType} tasks</p>
          <p class="state">${artisanData.state}</p> 
        </div>

        <div class="artisan-footer">
          <p class="experience">${artisan.experience}</p>
          <button type="button" value="${ artisan.user_id }" class="btn btn-info schedule-btn" data-bs-toggle="modal" data-bs-target="#staticBackdrop">
            Select and Continue
          </button> 
        </div>
      </div>
    `;
  }

  // Display artisan details in the modal
  $('.schedule-btn').on('click', function() {
    // Iterate over the artisans and their data, return data if artisan.user_id is equall to artisansUserData.id
    artisans.forEach((artisan, index) => {
      artisansUserData.forEach((userData, index) => {
        if (artisan.user_id == userData.id) {
          if (artisan.user_id == $(this).val()) {
            let firstName = userData.first_name
            let lastName = userData.last_name
            lastNameFirstletter = lastName[0].toUpperCase()
            $('.headerTexts').text(firstName + ' ' + lastNameFirstletter +'.' + "'s" + " Availability")
            $('.artisan-image').attr('src', '/static/images/craftdot_logo.webp', 'alt', firstName)
            $('.artisan-image').attr('alt', firstName)
          }
        }
      })
    })
  });

  // Date and Time Picker
  $('#timePicker').timepicker({
    timeFormat: 'h:mm p',
    interval: 30,
    minTime: '8:30am',
    maxTime: '6:00pm',
    defaultTime: '8:30am',
    startTime: '8:30am',
    dynamic: false,
    dropdown: true,
    scrollbar: true,
    zindex: 1060,
    change: function(time) {
      let timeText = $('#timePicker').val();
      $('.requestTime').text(timeText)
      // Send the time to html for processing
      $('#time').val(timeText)
    }
  });



  // Date Picker
  $( '#datePicker').datepicker({
    dateFormat: 'd MM, yy',
    minDate: '0',
    maxDate: '+2w',
    onUpdateDatepicker: function() {
      let dateText = $( '#datePicker').val()
      $('.requestDate').text(dateText)
      // Send the date to html for processing
      $('#date').val(dateText)
    },
  });



  // Pagination
  let currentPage = 1;
  const itemsPerPage = 3;
  let items = []; // This should be your list of items to paginate

  // Function to render items on the page
  function renderItems() {
      const list = $('#item-list');
      list.empty();
      const start = (currentPage - 1) * itemsPerPage;
      const end = start + itemsPerPage;
      const paginatedItems = items.slice(start, end);
      
      paginatedItems.forEach(item => {
          list.append(`<li>${item}</li>`);
      });
  }

  // Function to handle page change
  function goToPage(page) {
      currentPage = page;
      renderItems();
  }

  $('#prev').click(function(event) {
      event.preventDefault();
      if (currentPage > 1) {
          currentPage--;
          renderItems();
      }
  });

  $('#next').click(function(event) {
      event.preventDefault();
      if (currentPage < Math.ceil(items.length / itemsPerPage)) {
          currentPage++;
          renderItems();
      }
  });

  // Initialize with dummy data
  function initPagination() {
    // Assuming you fetch or have your items array ready
    items = [
        'Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5',
        'Item 6', 'Item 7', 'Item 8', 'Item 9', 'Item 10',
        // Add as many items as you need
    ];
    renderItems();
  }

  initPagination();

});