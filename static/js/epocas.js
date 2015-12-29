function getListElements(the_array, the_class){
	the_string = '';
	for(var j=0; j<the_array.length; j++){
		the_string += '<li class="invisible ficha '+the_class+'" id="movie-'+the_class+'">' + the_array[j] + '</li>';
	}
	return the_string;
}



$(document).ready(function () {

	$('#opts').click(function () {
		var value = document.getElementById('opts');
		value = value.options[value.selectedIndex].text;

		// Remove the container of the previously presented movies
		$('.img-poster-holder').remove();

		// Get the movies of that age via AJAX
		$.get('/califas/get_movies_by_age/', {value:value}, function (data){

			var lista = JSON.parse(data);

			console.log(lista)

			// media folder in aws:
			var aws_media = "http://cinesnob-images.s3.amazonaws.com/";

			if(lista && lista[0]){
				for(var i = 0; i < lista.length; i+=1){
					var lstars = parseInt(lista[i]['rating']);
					lstars = paintStars(lstars);

					var poster_path = (lista[i]["poster"]!="")
											? aws_media + lista[i]["poster"]
											: "../images/default.jpg";

					var imagen = '<img class="ficha img-big" id="mi-imagen" src="'+ poster_path +'"/>'

					// Put my div in the DOM
					var img_poster_holder =
					'<div class="img-poster-holder movie-detail" id="'+ lista[i]['slug'] + '">'+imagen +'<br />'+
'<p class="ficha movie-name" data-title="'+lista[i]['movie_name']+'"><a title="'+lista[i]['movie_name']+'" alt="'+lista[i]['movie_name']+'"> '+lista[i]['movie_name']+'</a></p>'+
					'<p class="ficha rating" data-rating="'+lista[i]['rating']+'">' + lstars + '</p>'+
					'<p class="invisible ficha" id="movie-director">' + lista[i]['director'] + '</p>'+
					'<ul>';
					var genre_array = lista[i]['genre'];
					img_poster_holder += getListElements(genre_array, 'genres');
					img_poster_holder += '</ul>'+
					'<p class="invisible ficha" id="movie-year">'  + lista[i]['year']+'</p>'+
					'<ul>';
					var opinion_array = lista[i]['opinion'];
					img_poster_holder += getListElements(opinion_array, 'opinions');
					img_poster_holder += '</ul>'+
					'<p class="invisible ficha">' + poster_path + '</p></div>';
					$(img_poster_holder).appendTo("#posters-container");
				}
			}
			else {
				$('<div class="img-poster-holder">' +
					"No hay películas de esta época.<br/>"
				 ).appendTo("#posters-container");
			}


	// If a title is too long, shorten it
	var all_titles = $('.movie-name').map(function(){
		console.log("ujule");
		var current_title = $(this).find('a');//.text();
		// current_title.text("cabronazo!");
		if(current_title.text().length > 20){
			var shortened_title = current_title.text().slice(0, 17)+'...';
			// console.log(shortened_title);
			current_title.text(shortened_title);
			// console.log(current_title);
			// $(this).
			// $(this).html(shortened_title);
		}
	})


		});
	});
});
