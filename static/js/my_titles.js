
// This code snippet is from the django documentation https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name){
	var cookieValue = null;
	if(document.cookie && document.cookie != ''){
		var cookies = document.cookie.split(';');
		for(var i=0; i<cookies.length; i++){
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if(cookie.substring(0, name.length + 1) == (name + '=')){
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

var edit_delete = '<span class="edit-title">Edit</span> <span class="delete-title">Delete</span>';

$(function(){

	$('.movie-detail').each(function(){
		$(this).append(edit_delete);
	});

	$('.delete-title').on('click', function(event){
		event.stopPropagation();
		var csrftoken = getCookie('csrftoken');
		console.log(csrftoken);
		var current_title = $(this).parent();
		var title = $(this).parent().find('.movie-name').attr('data-title');

		var delete_title = confirm("¿Quieres borrar "+title+" de tu biblioteca?");
		if(delete_title){
			$.post('/califas/delete_title/', {value: title, csrfmiddlewaretoken: csrftoken}, function (data){
				current_title.remove();
			});
		}
	});
	// $('.movie-detail img').on('mouseover', function(){
	// 	console.log("Over");
	// 	$(this).css({border:'5px solid yellow'});
	// });

	// $('.movie-detail img').on('mouseout', function(){
	// 	console.log("Out");
	// 	$(this).css({border:'0'});
	// });

});