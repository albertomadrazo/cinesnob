// /////////////////////////////////////////////////////////////////////////
$(document).ready(function(){
	$('.menu').on('mouseover', function(){
		//alert("perros");
		$(this).next('.submenu').css({'visibility': 'visible'});
	});


	$('.submenu').on('mouseover', function(){
		$(this).css({'visibility': 'visible'});
	});

	$('.submenu').on('mouseout', function(){
		$(this).css({'visibility': 'hidden'});
	});
});