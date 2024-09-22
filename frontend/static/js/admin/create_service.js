$( document ).ready(function() {



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

	// Update the service icon 
	$('#serviceIcon').on('click', function() {
		$('#inputIcon').click();
	});
	$('#inputIcon').on('change', function(e) {
		const file = e.target.files[0]
		if (file) {
			const reader = new FileReader();
			reader.onload = function(e) {
				$('#serviceIcon').attr('src', e.target.result);
			};
			reader.readAsDataURL(file);
		}
	});

	$("#add-item-button").click(function() {
		const input = $('<input type="text" name="data_list[]" placeholder="Enter item" required>');
		$("#data-list-container").append(input);
});

});