function fillArr(arr, val){
	var i;
	for(i=0;i<arr.length;i+=1) arr[i] = val;
	return arr;
};

var overmenu = fillArr( new Array(4), false);
var oversub = fillArr( new Array(4), false);

$(document).ready(function(){
	var subNumber;
	var currentSub;

	$('.menu-element').on('mouseover', function(){
		subNumber = parseInt($(this).attr('value'));

		$('#submenu'+subNumber).css('display', 'block');
		currentSub = '#submenu'+subNumber;
		overmenu[subNumber] = true;
	});

	$('.menu-element').on('mouseout', function(){
		subNumber = parseInt($(this).attr('value'));
		overmenu[subNumber] = false;
		if( oversub[subNumber] === false){
			$('#submenu'+subNumber).css('display', 'none');	
			overmenu[subNumber] = false;	
		}
		else {
			$('#submenu'+subNumber).css('display', 'block');
			oversub[subNumber] = true;
		}
	});

	$('.sub').on('mouseover', function(){
		$(this).css('display', 'block');
		oversub[subNumber] = true;

	});
	$('.sub').on('mouseout', function(){
		if( overmenu[subNumber] === false ){
			$(this).css('display', 'none');
		}
		oversub[subNumber] = false;
	});
});