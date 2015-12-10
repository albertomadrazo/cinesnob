// function paintStars(rating){
// 	var stars = '';
// 	for(var i=0; i<rating;i++){ 
// 		stars += '<img src="/static/images/star.png">'; 
// 	}

// 	stars = '<p class="format-stars">'+stars+'</p>';

// 	return stars;
// }

$(document).ready(function () {

	$('#opts').click(function () {

		var value = document.getElementById('opts');
		value = value.options[value.selectedIndex].text;

		// Remove the container of the previously presented movies
		$('.img-poster-holder').remove();

		$.get('/califas/get_movies_by_age/', {value:value}, function (data){
		
			var lista = JSON.parse(data);

			console.log(lista)

			if(lista && lista[0]){
				for(var i = 0; i < lista.length; i+=1){
					var lstars = parseInt(lista[i]['rating']);
					lstars = paintStars(lstars);

					var poster_path = (lista[i]["poster"]!="")
											? "../../media/" + lista[i]["poster"]
											: "../images/default.jpg";

					var imagen = '<img class="ficha img-big" id="mi-imagen" src="'+ poster_path +'"/>'

					// Put my div in the DOM
					$('<div class="img-poster-holder movie-detail" id="'+ lista[i]['slug'] + '">'  +
					  							    											  imagen + 
					  							  												'<br />' +
		  '<p class="ficha" id="movie-name">' + lista[i]['movie_name'] + '</p>' +
			'<p class="ficha rating" data-rating="'+lista[i]['rating']+'">' + lstars + '</p>'+
					  	     '<p class="invisible ficha" id="movie-director">' + lista[i]['director'] + '</p>'     +
					 		 '<p class="invisible ficha" id="movie-genre">' + lista[i]['genre'] + '</p>' +
					         '<p class="invisible ficha" id="movie-year">'  + lista[i]['year']+'</p>'    +
					   '<p class="invisible ficha" id="movie-review">' + lista[i]['opinion']+ '</p>'      +
					   '<p class="invisible ficha">' + poster_path + '</p></div>'
						).appendTo("#posters-container");
				}
			}
			else {
				$('<div class="img-poster-holder">' +
					"No hay películas de esta época.<br/>"
				 ).appendTo("#posters-container");
			}

		});
	});
});