$(document).ready(function () {

	$('#opts').click(function () {

		var value = document.getElementById('opts');
		value = value.options[value.selectedIndex].text;

		// Remove the container of the previously presented movies
		$('.img-poster-holder').remove();

		$.get('/califas/get_movies_by_age/', {value:value}, function (data){
		
			var lista = JSON.parse(data);

			if(lista and lista[0]){
				for(var i = 0; i < lista.length; i+=1){

					var poster_path = (lista[i]["poster"]!="")
											? "../../media/" + lista[i]["poster"]
											: "../images/default.jpg";

					var imagen = '<img class="ficha img-big" id="mi-imagen" src="'+ poster_path +'"/>'

					// Put my div in the DOM
					$('<div class="img-poster-holder movie-detail" id="'+ lista[i]['movie_name'] + '">'  +
					  							    											  imagen + 
					  							  												'<br />' +
		  '<p class="ficha" id="movie-name">' + lista[i]['movie_name'] + '</p>' +
					     '<p class="ficha" id="'+ lista[i]['rating'] + '">' + lista[i]['rating'] + '</p>'+
					  	     '<p class="ficha" id="movie-director">' + lista[i]['director'] + '</p>'     +
					 		 '<p class="invisible ficha" id="movie-genre">' + lista[i]['genre'] + '</p>' +
					         '<p class="invisible ficha" id="movie-year">'  + lista[i]['year']+'</p>'    +
					   '<p class="invisible ficha" id="movie-review">' + lista[i]['review']+ '</p>'      +
					   '<p class="invisible ficha">' + poster_path + '</p></div>'
						).appendTo("#movies-container");
				}
			}
			else {
				$('<div class="img-poster-holder">' +
					"No hay películas de esta época.<br/>"
				 ).appendTo("#movies-container");
			}

		});
	});
});