import atexit
from random import randint

from neopixel import *

# LED strip configuration:
LED_COUNT      = 299     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_CHANNEL    = 0       # PWM channel
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

class LedColors:
    def __init__(self):
        self.colors = {
            'Red': Color(0, 255, 0),
            'Yellow': Color(255,255,0),
            'Green': Color(255, 0, 0),
            'Cyan': Color(2550,0,255),
            'Blue': Color(0,0,255),
            'Magenta': Color(0,255,255),
            'White': Color(255,255,255),
            'Black': Color(0, 0, 0)
            }

        self.color_index = 0

    def get(self, key):
        return self.colors.get(key)

    def cycle(self):
        color = self.colors.values()[self.color_index]
        self.color_index += 1
        if(self.color_index >= len(self.colors.keys())):
            self.color_index = 0
        return color

    def random(self):
        return Color(self.__randint_for_color(), self.__randint_for_color(), self.__randint_for_color())

    def __randint_for_color(self):
        return randint(0, 255)/randint(1,10)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

led_colors = LedColors() 

def brightness(b=60):
    if 0 <= b <= 255:
        strip.setBrightness(b)
    else:
        raise ValueError('Brightness must be between 0 and 255')

def get_brightness():
    return strip.getBrightness()

def clear():
    """Clear the buffer"""
    for x in range(length()):
        set_pixel(x, led_colors.get("Black"))

def off():
    clear()
    show()

def set_pixel(x=0, color=led_colors.get('White')):
    if x is not None:
        strip.setPixelColor(x, color)

def set_all_pixels(color=led_colors.get("White")):
    for x in range(length()):
        strip.setPixelColor(x, color)

def get_pixel(pixel):
    if 0 < pixel <= length(): 
        return strip.getPixelColor(pixel)

def get_pixels():
    return [get_pixel(x) for x in range(length()+1)]

def show():
    strip.show()
 
def length():
    return strip.numPixels()

def ColorToRGB(color):
	print(color)
	green = color >> 16
	print(color)
    red = color >> 16 & color >> 8 
	print(color)
    blue = color >> 16 & color >> 8 & color
	print(color)


    print(color,red,green,blue)
    return (red,green,blue)

def _clean_shutdown():
    off()

off()
atexit.register(_clean_shutdown)
