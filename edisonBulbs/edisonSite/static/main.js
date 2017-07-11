$( document ).ready(function() {
    $.get('/status/')
	.done(function(data){data.forEach(setLightCss)})
});

function toggleBulb(bulb){
	$.get('/toggle/' + bulb)
	.done(function(data){data.forEach(setLightCss)})
}

function allOn(){
	$.get('/all/on/')
	.done(function(data){data.forEach(setLightCss)})
}

function allOff(){
	$.get('/all/off/')
	.done(function(data){data.forEach(setLightCss)})
}

function setLightCss(element, index, array){
	var light = $('.fa-lightbulb-o').eq(index)
	if (element == 1 && !light.hasClass("light_on")){light.addClass("light_on")}
	else if (element == 0 && light.hasClass("light_on")){light.removeClass("light_on")}
}

function setRoutine(){
	var routine = $('#routines label.active input').val()
	var seconds = $('#secondsInput').val()
	var secondsModifier = $('#secondsModifier').val()
	var delay = seconds * secondsModifier
	$.get('/routine/'+routine+'/'+delay)
}