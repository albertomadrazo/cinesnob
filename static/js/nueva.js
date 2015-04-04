/* TODO: 
  -evitar que se vaya sin escribir un genero
*/
var globos = { 'generoSeleccionado': false };

/*$('#your_rating :checkbox').click(function(){

	var rating = $(this).id;
	$('#your_rating :checkbox[value=4]').attr('checked', true);
	alert(rating);
});

function molocho(){
	return "Pedazo de chingon";
}*/

function prueba(){
	return "jolines";
	//$('#your_rating :radio')
}

function starMeter(rating){
	//var rating = $("input[type='checkbox']:checked").val();
	//var rating = $("#your_rating checkbox").value;
	//alert(rating)
	//alert(rating);
	if((rating<1) && (rating>5)){
		return;
	}
		
	//STARS_APP.starsNumber = rating;
	//					0      1      2       3       4         5
	var starArray = ['cero', 'uno', 'dos', 'tres', 'cuatro', 'cinco'];
	for(var a=rating; a>=1; a-=1){
		//$(starArray[a]).checked(true);
		console.log("--"+a);
		document.getElementById(starArray[a]).checked = true;
	}

	for(var b=rating+1; b<=5; b+=1){
		//$("input[type='radio']").val(b).checked(false);
		console.log(b);
		console.log(starArray[b]);
		document.getElementById(starArray[b]).checked = false;
	}
	$('#estrellas_'+(rating-1)).attr('checked', 'checked');
	//alert('#estrellas_'+(rating));
}

function addNewGenre(){
	if(globos['generoSeleccionado'] === true){
		$('#nueva').remove();
	}
	$('#new-option, #new-option-button').toggle();

	if($('#new-option').val() == ''){
		alert('rero');
		$('#new-option').val("Rocio");
		globos['generoSeleccionado'] = false;
	}

	$('#opciones option:last').before('<option id="nueva">'+ $('#new-option').val() +'</option>');
	$('#nueva').prop('selected', true);
	$('#opciones').toggle();
	$('#new-option, #new-option-button').remove();
	globos['generoSeleccionado'] = true;
}
function reddy(){
	alert("ready!!!!");
}

$(document).ready(function(){

	$('#opciones').click(function(){

		var e = document.getElementById('opciones');
		var whichOption = e.options[e.selectedIndex].text;
		if(whichOption === "otro"){
			$("#opciones").toggle();
			$('#cont-opciones').append("<input type ='text' id='new-option' placeholder='genero' />");
			$('#cont-opciones').append("<div id='new-option-button' onclick='addNewGenre();'>Enter genre</div>");
		}
	});
});