// This code seems to be obsolete!
$(document).ready(function(){
	$('.menu').on('mouseover', function(){
		$(this).next('.submenu').css({'visibility': 'visible'});
	});


	$('.submenu').on('mouseover', function(){
		$(this).css({'visibility': 'visible'});
	});

	$('.submenu').on('mouseout', function(){
		$(this).css({'visibility': 'hidden'});
	});
});