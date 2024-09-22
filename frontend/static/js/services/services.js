$( document ).ready(function () {
	// Confirm the appliction is loaded, hide loading spinner and unblur
  setTimeout( function() {
    console.log('load')
    $('.container-spinner').hide()
    $('#main-cont, #header-cont').removeClass("blurred");
  })
  // Create service card
  function createServiceCard(service) {
    return `
      <a href="#">
        <div class="card">
          <div class="card-footer">
            <p class="text-body-secondary text-bold">${ service.name }</p>
          </div>
        </div>
      </a>
    `;
  }
  // Extract data from the embedded JSON
  const services = JSON.parse($('#services').html());

  
  // Dynamically update the available artisans
  const availableServices = () => {
    services.forEach((service) => {
      $('#service-card').append(createServiceCard(service));
    });
  }

  availableServices();
    
});