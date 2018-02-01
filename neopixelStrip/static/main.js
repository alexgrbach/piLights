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
            if (!isDone){
                isDone = true;
                setContainerColor(startPixel, endPixel, e.color._r.toFixed(),e.color._g.toFixed(),e.color._b.toFixed())
                $.ajax({
                    url: '/pixel/set/array',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(container),
                    dataType: 'json'
                }).done(function(data){
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
        update(data)
    }); 
}

function update(data){
    container = data;
    $('#brightness_slider').val(data.brightness);
    $('#colorArray').children().each(function(index){$(this).css({'color': 'rgb(' + data.stripColors[index] + ')'});});

}

//New stuff
//
//
//

function sortNumbers(object){
    return object.sort(function(a, b){return a-b})
}


function generateRainbow(start, end, frequency1, frequency2, frequency3, phase1, phase2, phase3){
    if (frequency1 == undefined) frequency1 = .3;
    if (frequency2 == undefined) frequency2 = .3;
    if (frequency3 == undefined) frequency3 = .3;
    if (phase1 == undefined) phase1 = 0;
    if (phase2 == undefined) phase2 = 2;
    if (phase3 == undefined) phase3 = 4;
    phase1 = phase1 * Math.PI / 3
    phase2 = phase2 * Math.PI / 3
    phase3 = phase3 * Math.PI / 3

    var stepSize = 20/Math.abs(end - start);

    var step = 0.0;
    var pixel = container.stripColors;
    var sorted = sortNumbers([start, end]);

    for (var i = 0; i < container.numberOfBulbs; ++i)
    {
        if (i >= sorted[0] && i <= sorted[1]) {
            var r = (Math.sin(frequency1*step + phase1) * 127 + 128).toFixed();
            var g = (Math.sin(frequency2*step + phase2) * 127 + 128).toFixed();
            var b = (Math.sin(frequency3*step + phase3) * 127 + 128).toFixed();
            container.stripColors[i] = [r,g,b]
            step += stepSize
        }
    }   
    updateStripArray()
}

function setContainerColor(start,end,r,g,b){
    var sorted = sortNumbers([start, end]);
    for (var i = 0; i < container.numberOfBulbs; ++i){
        if (i >= sorted[0] && i <= sorted[1]) { container.stripColors[i] = [r,g,b]; }
    }
}

function updateStripArray(){
    $.ajax({
        url: '/pixel/set/array',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(container),
        dataType: 'json'
    }).done(function(data){
        update(data)
    });
}


function setBrightness(brightness){
    $.get('/brightness/set/' + brightness)
}

function allOff(){
    $.get('/off')
    .done(function(data){update(data)});
}