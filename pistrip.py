import atexit
from random import randint

from neopixel import *

# LED strip configuration:
LED_COUNT      = 300      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_CHANNEL    = 0       # PWM channel
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()
   
class LedColors:
    def __init__(self):
        self.colors = {
            'Red': Color(255, 0, 0),
            'Green': Color(0, 255, 0),
            'Blue': Color(0,0,255),
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



led_colors = LedColors()





def _clean_shutdown():
    """Registered at exit to ensure strip cleans up after itself
    and all pixels are turned off.
    """
    off()

def brightness(b=60):
    """Set the display brightness between 0.0 and 1.0

    :param b: Brightness from 0.0 to 1.0 (default 0.2)
    """

    if b > 256 or b < -1:
        raise ValueError('Brightness must be between 0.0 and 1.0')

    brightness = b
    # if brightness < 60:
    #     print("Warning: Low brightness chosen, your strip might not light up!")

    strip.setBrightness(brightness)

def get_brightness():
    """Get the display brightness value

    Returns a float between 0.0 and 1.0
    """
    return round(strip.getBrightness()/255.0, 3)

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

# def get_pixel(i, r, g, b):
#     if i is not None: 
#         pixel = strip.getPixelColor(i)
#         return int(pixel.r), int(pixel.g), int(pixel.b)

def get_pixels():
    return [get_pixel(x) for x in range(length())]

def show():
    strip.show()

def length():
    return strip.numPixels()

atexit.register(_clean_shutdown)
