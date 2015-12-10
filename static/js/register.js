var image = (function($){
	function readURL(input){
		if(input.files && input.files[0]){
			var reader = new FileReader();

			reader.onload = function(e){
				var loaded_img = '<img id="preview-avatar" src="'+e.target.result+'">';
				// loaded_img.attr('id', 'preview-avatar');
				// loaded_img.attr('src', e.target.result);
				$('#avatar-container').append(loaded_img);
				// $('#preview-avatar').css({opacity:'1.0'});
				// $('#preview-avatar').animate({opacity: ''}, 2000);
				$('#preview-avatar').css('visibility', 'visible').hide().fadeIn('200');
			}

			reader.readAsDataURL(input.files[0]);
		}
	}

	return {
		readURL: readURL
	};
})(jQuery);

$(document).ready(function(){
	$('#id_avatar').on('change', function(){
		$(this).attr('name', "Cambiar Imágen");
		image.readURL(this);
	});
});