import atexit
import RPi.GPIO as GPIO
from random import randint

chan_list = [7,11,13,15,29,31,33,37]

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(chan_list, GPIO.OUT, initial=GPIO.LOW)

def toggle_random_bulbs():
	number_of_bulbs = randint(1,7)
	chans = list(chan_list)
	for bulbs in range(0, number_of_bulbs):
		bulb = randint(0, len(chans) - 1)
		toggle_bulb(chans[bulb])
		chans.remove(chans[bulb])

def toggle_bulb(bulb):
	GPIO.output(bulb, not GPIO.input(bulb))

def get_random_bulb():
	return chan_list[randint(0,7)]

def _clean_shutdown():
	GPIO.cleanup()

atexit.register(_clean_shutdown)