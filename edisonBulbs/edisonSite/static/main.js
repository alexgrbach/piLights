$( document ).ready(function() {
    $.get('/status/')
	.done(function(data){bulbStatus(data)})
});

function toggleBulb(bulb){
	$.get('/toggle/' + bulb)
	.done(function(data){bulbStatus(data)})
}

function allOn(){
	$.get('/all/on/')
	.done(function(data){bulbStatus(data)})
}

function allOff(){
	$.get('/all/off/')
	.done(function(data){bulbStatus(data)})
}

function bulbStatus(bulbs){
	console.log(bulbs)
	bulbs.forEach(setLightCss)
}

function setLightCss(element, index, array){
	var light = $('.fa-lightbulb-o').eq(index)
	if (element == 1 && !light.hasClass("light_on")){light.addClass("light_on")}
	else if (element == 0 && light.hasClass("light_on")){light.removeClass("light_on")}
}