$(document).ready(function () {
	$('#opts').click(function () {

		var value = document.getElementById('opts');
		value = value.options[value.selectedIndex].text;

		$('.img-poster-holder').remove();

		$.get('/califas/get_movies_by_age/', {value:value}, function (data){
		
			var lista = JSON.parse(data);
			if(lista != ""){
				for(var i = 0; i < lista.length; i+=1){
					var imagen = (lista[i]["poster"]!="")?'<img class="img-big" src="../../media/'+lista[i]["poster"]+'"/>':
					  '<img class="img-big" src="../../static/images/default.jpg"/>';
					 // alert(imagen);
					$('<div class="img-poster-holder">'  +
					  							  imagen +
					  '<p>'+lista[i]['movie_name']+'</p>'+
					  '<p>'+lista[i]['year']+'</p>'      +
					  '<p>'+lista[i]['director']+'</p>'
						).appendTo("#movies-container");
				}
			}
			else {
				$('<div class="img-poster-holder">' +
					"No hay películas de esta época :(<br/>"
				 ).appendTo("#movies-container");
			}

		});
	});
});