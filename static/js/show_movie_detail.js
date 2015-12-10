function paintStars(rating){
	var stars = '';
	for(var i=0; i<rating;i++){ 
		stars += '<img src="/static/images/star.png">'; 
	}

	stars = '<span class="format-stars">'+stars+'</span>';

	return stars;
}

$(document).ready(function(){

	var all_ratings = $('.rating').map(function(){
		var current_rating = $(this).attr('data-rating');
		current_rating = parseInt(current_rating);
		var title_rating = paintStars(current_rating);
		$(this).append(title_rating);
		
	})

	$(document).on('click', '.movie-detail', function(){
		// Makes the popup visible

		$('div#movie-pop-container').css('visibility', 'visible');

		// Pickup all the vars from the div
		var pop = $('div#movie-pop-contents');
		console.log(pop+"fuck");
		var title    = $(this).children('p').eq(0).text();
		var rating   = $(this).children('p').eq(1).attr('data-rating');
		var director = $(this).children('p').eq(2).text();
		var genre    = $(this).children('p').eq(3).text();
		var year     = $(this).children('p').eq(4).text();
		var opinion  = $(this).children('p').eq(5).text();
		var poster   = $(this).children('p').eq(6).text();
		var stars    = '';
		// alert(poster);
		rating = parseInt(rating);
		// append one star image per point of rating and put them inside a paragraph
		stars = paintStars(rating);
		// $('div#movie-review').removeClass('invisible');
		// alert(year);
		pop.append(
			'<div id="ficha">'
				+'<h2 id="rr">'+title+'</h2>'
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
			+'<div id="opinion">'
				+'<p>'+opinion+'</p>'
			+'</div>'
		);	
	});
	

	$('div#movie-pop-close, div#movie-pop-veil').click(function(){
		$('div#movie-pop-contents').empty();
		$('div#movie-pop-container').css('visibility', 'hidden');
		// $('div#movie-review').addClass('invisible');
	});

});