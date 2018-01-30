var container = {}

var startPixel = 0;
var endPixel = 0;
var color = []
var bulbSelected =false;

$(window).on('load',function(e){
	 $('.fa-circle').mousedown(function(){ selectRange($(this)); });
	 $('.fa-circle').hover(function(){setHover($(this))})
});

function selectRange(control){
	var index = control.attr('index');
	var pos = control.position()
 
	if(!bulbSelected){
		startPixel = index;
		$('.fa-circle').eq(index).addClass('bulbSelected');
		bulbSelected = true;
		// $('.colorPicker input').val(color)
	}
	else if(bulbSelected){
		endPixel =  index;
		var isDone = false; 
		bulbSelected = false;

		control.colorpicker({
	      color: control.css('color'),
	      inline: true,
	      container: true,
	      format:"rgb"
	    }).on('colorpickerChange', function (e) {

	    console.log(`rgb(${e.color._r.toFixed()},${e.color._g.toFixed()},${e.color._b.toFixed()})`)	    	
	    	if (!isDone){
	    		isDone = true;
	    		$.get(`/pixel/set/range/${startPixel}/${endPixel}/${e.color._r.toFixed()}/${e.color._g.toFixed()}/${e.color._b.toFixed()}/`)
					.done(function(data){
						container = data;
						update(data);
						isDone = false;
					});
    			}
	    	});
	    $('div.colorpicker').css({'top':pos.top+15, 'left':pos.left})
		$('.shade').show()
	}
};

function setHover(control){
	var bulbs = $('.fa-circle');
	$('.fa-circle').each(function(){$(this).removeClass('bulbSelected')});

	if (bulbSelected){
		var hoverLocation = parseInt(control.attr('index'));
		// console.log(hoverLocation)
		if (hoverLocation > startPixel){
			for (var i = startPixel - 1; i < hoverLocation; i++) {
				$('.fa-circle').eq(i + 1).addClass('bulbSelected');
			}
		}
		else if (hoverLocation < startPixel) {
			// console.log(`startPixel: ${startPixel}\thoverLocation: ${hoverLocation}`);
			for (var i = startPixel; i >= hoverLocation; i--) {
				$('.fa-circle').eq(i).addClass('bulbSelected');
			}
		}
		else {
			control.addClass('bulbSelected')
		}				
	}
};

$('.shade').mousedown(function(){
	$(this).hide();
	$('.fa-circle.colorpicker-element').colorpicker('destroy'); 
	// getStatus();
});




$('#brightness_slider').on('input', function(){
	$.get('/brightness/set/'+$(this).val())
});


$( document ).ready(function(){
	getStatus();
});

function getStatus(){
	    $.get('/status')
	.done(function(data){
		container = data
		update(data)
	});	
}

function update(data){
	$('#brightness_slider').val(data.brightness);
	$('#colorArray').children().each(function(index){$(this).css({'color': 'rgb(' + data.stripColors[index].join(', ') + ')'});});

}





function makeColorGradient(frequency1, frequency2, frequency3,
                             phase1, phase2, phase3,
                             center, width)
  {
    if (center == undefined)   center = 128;
    if (width == undefined)    width = 127;
    var done = false;
    for (var i = 0; i < container.numberOfBulbs; ++i)
    {
       var r = (Math.sin(frequency1*i + phase1) * width + center).toFixed();
       var g = (Math.sin(frequency2*i + phase2) * width + center).toFixed();
       var b = (Math.sin(frequency3*i + phase3) * width + center).toFixed();
       $.get(`/pixel/set/single/${i}/${r}/${g}/${b}`).done(function(data){
				container = data;
				update(data);
			});
    }
  }

// function setRange(startPixel, endPixel){
// 	var rgb = $('div.colorpicker').val()
// 	rgb = rgb.substring(4, rgb.length-1).replace(/, /g, "/")
// 	$.get(`/pixel/set/range/${startPixel}/${endPixel}/${rgb}/`)
// 	.done(function(data){
// 		container = data
// 		update(data)
// 	})
// }

function buildColorArray(jsonData){
	//<i class="fas fa-circle" style="color:red"></i>
	$('#colorArray').append(jsonData.stripHTML)
	
	//jsonData.stripColors.forEach(function(data, index){$('#colorArray').append(jasonData.stripHTML)})
}

function toggleBulb(bulb){
	$.get('/toggle/' + bulb)
	.done(function(data){data.forEach(setLightCss)});
}

function setBrightness(brightness){
	$.get('/brightness/set/' + brightness)
	// .done(function(data){$('something').innerHtml(data.responseJSON.brightness)})
}

function allOff(){
	$.get('/off')
	.done(function(data){update(data)});
}


// function setLightCss(element, index, array){
// 	var light = $('.fa-lightbulb-o').eq(index)
// 	if (element == 1 && !light.hasClass("light_on")){light.addClass("light_on")}
// 	else if (element == 0 && light.hasClass("light_on")){light.removeClass("light_on")}
// }

// function setRoutine(){
// 	var routine = $('#routines label.active input').val()
// 	var seconds = $('#secondsInput').val()
// 	var secondsModifier = $('#secondsModifier').val()
// 	var delay = seconds * secondsModifier
// 	$.get('/routine/'+routine+'/'+delay)
// }