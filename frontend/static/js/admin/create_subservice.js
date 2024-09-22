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

});