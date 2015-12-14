var image = (function($){
	function readURL(input){
		if((input.files) && input.files[0]){
			var reader = new FileReader();
			reader.readAsDataURL(input.files[0]);

			reader.onload = function(e){
				var loaded_img = '<img id="preview-avatar" src="'+e.target.result+'">';
				$('#avatar-container').empty();
				$('#avatar-container').append(loaded_img);
				$('#preview-avatar').css('visibility', 'visible').hide().fadeIn('200');
			}
		}
	};

	return {
		readURL: readURL
	};
})(jQuery);

$(document).ready(function(){
	$('#id_avatar, #id_poster').on('change', function(){
		image.readURL(this);
	});
});