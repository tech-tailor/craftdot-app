$( document ).ready(function() {

	
	// Extract services from the embedded JSON
	const serviceList = JSON.parse($('#serviceList').html());

	// Get random service name
	randomService = serviceList[Math.floor(Math.random() * serviceList.length)];
	const serviceName = randomService.name

	var escapeName = serviceName.replace(/ /g, '\\ ')
	console.log(escapeName)
	// Show one random service
	$('#' + `${escapeName}`).show();

	// Change service name color
	$(".sub-item").css('color', 'black');


	$('.sub-item, service-icon').on('click', function() {
		$(".content").hide();

		
		
		let service = $(this).data('content');
		
		// Replace spaces in the service name
		var escapeName = service.replace(/ /g, '\\ ')
		
		console.log('#' + `${escapeName}service`)
		$('#' + `${escapeName}`).show();
		$('.sub-item').css('color', 'black');
		$('.sub-item').css('backgroundColor', 'white')
		$('#' + `${escapeName}service`).css('color', 'white');
		$('#' + `${escapeName}service`).css('backgroundColor', 'black')
		
	})

});