$(document).ready(function(){


	$(document).on('click', '.movie-detail', function(){
		// Makes the popup visible

		$('div#movie-pop-container').css('visibility', 'visible');

		// Pickup all the vars from the div
		var pop = $('div#movie-pop-contents');
		console.log(pop+"fuck");
		var titulo   = $(this).children('p').eq(0).text();
		var rating   = $(this).children('p').eq(1).text();
		var director = $(this).children('p').eq(2).text();
		var genre    = $(this).children('p').eq(3).text();
		var year     = $(this).children('p').eq(4).text();
		var review   = $(this).children('p').eq(5).text();
		var poster   = $(this).children('p').eq(6).text();
		var stars    = '';
		// alert(poster);
		rating = parseInt(rating);
		// append one star image per point of rating and put them inside a paragraph
		for(var i=0; i<rating;i++)
			{ stars += '<img src="/static/images/star.png" />'; }
		stars = '<p id="rating">'+stars+'</p>';

		pop.append(
			'<div id="ficha">'
				+'<h2 id="rr">'+titulo+'</h2>'
				+'<p id="ddd">Director: <strong>'+director+'</strong><br/>'
				   +'Año: <strong>'+year+'</strong><br/>'
				   +'Género: <strong>'+genre+'</strong><br/>'
				   +'<p id="rating">'+stars
				   +'</p>'
				+'</p>'
			+'</div>'
			+'<div id="poster-big">'
			+'<img id="poster" src="'+poster+'"/>'
			+'</div>'
			+'<div id="review">'
				+'<p>'+review+'</p>'
			+'</div>'
		);	
	});
	

	$('div#movie-pop-close, div#movie-pop-veil').click(function(){
		$('div#movie-pop-contents').empty();
		$('div#movie-pop-container').css('visibility', 'hidden');
	});

});