function paintStars(rating){
	var stars = '';
	for(var i=0; i<rating;i++){ 
		stars += '<img src="/static/images/star.png">'; 
	}
	stars = '<span class="format-stars">'+stars+'</span>';
	return stars;
}

function shortenTitleName(){
	var all_titles = $('.movie-name').map(function(){
		var current_title = $(this).find('a');//.text();
		if(current_title.text().length > 20){
			var shortened_title = current_title.text().slice(0, 17)+'...';
			current_title.text(shortened_title);
		}
	});
}

function convertPythonListIntoArray(jQuery, that, element){

	var elements = [];
	var single_element = that.find(element).each(function(){
		var current_element = $(this);
		elements.push(current_element.text());
	});
	return elements;
}

function getRandomElementFromArray(elements){
	var random_element = elements[Math.floor(Math.random() * elements.length)];
	return random_element;
}

$(document).ready(function(){

	// If a title is too long, shorten it
	shortenTitleName();

	// change the rating from numbers to stars
	var all_ratings = $('.rating').map(function(){
		var current_rating = $(this).attr('data-rating');
		current_rating = parseInt(current_rating);
		var title_rating = paintStars(current_rating);
		$(this).append(title_rating);
	});

	$(document).on('click', '.movie-detail', function(){
		// Make the popup visible
		$('div#movie-pop-container').css('visibility', 'visible');

		// Pickup all the vars from .movie-detail
		var reviews = []
		var pop = $('div#movie-pop-contents');
		var title    = $(this).children('p').eq(0).attr('data-title');
		var rating   = $(this).children('p').eq(1).attr('data-rating');
		var director = $(this).children('p').eq(2).text();
		var year     = $(this).children('p').eq(3).text();
		var poster   = $(this).children('p').eq(4).text();
		var stars    = '';
		// Convert the Python lists into JavaScript arrays
		var opinion = convertPythonListIntoArray($, $(this), '.opinions');
		opinion = getRandomElementFromArray(opinion);

		var genre = convertPythonListIntoArray($, $(this), '.genres');
		genre = getRandomElementFromArray(genre);

		// append one star image per point of rating
		stars = paintStars(parseInt(rating));

		pop.append(
			'<div id="ficha">'
				+'<h1 id="rr">'+title+'</h1>'
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
	});
});