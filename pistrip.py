import atexit

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

def _clean_shutdown():
    """Registered at exit to ensure strip cleans up after itself
    and all pixels are turned off.
    """
    off()

def brightness(b=0.3):
    """Set the display brightness between 0.0 and 1.0

    :param b: Brightness from 0.0 to 1.0 (default 0.2)
    """

    if b > 1 or b < 0:
        raise ValueError('Brightness must be between 0.0 and 1.0')

    brightness = int(b*255.0)
    if brightness < 60:
        print("Warning: Low brightness chosen, your strip might not light up!")

    strip.setBrightness(brightness)

def get_brightness():
    """Get the display brightness value

    Returns a float between 0.0 and 1.0
    """
    return round(strip.getBrightness()/255.0, 3)

def clear():
    """Clear the buffer"""
    for x in range(length()):
        strip.setPixelColorRGB(x, 0, 0, 0)

def off():
    clear()
    show()

def set_pixel(i, r, g, b):
    if i is not None:
        strip.setPixelColorRGB(i, r, g, b)

def set_all_pixels(r, g, b):
    for x in range(length()):
        strip.setPixelColorRGB(x, r, g, b)

def get_pixel(i, r, g, b):
    if i is not None:
        pixel = strip.getPixelColor(i)
        return int(pixel.r), int(pixel.g), int(pixel.b)

def get_pixels():
    return [get_pixel(i) for i in range(length())]

def show():
    strip.show()

def length():
    return strip.numPixels()

atexit.register(_clean_shutdown)
