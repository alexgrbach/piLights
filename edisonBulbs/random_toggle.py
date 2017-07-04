import time
import RPi.GPIO as GPIO
from random import randint
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

chan_list = [7,11,13,15,29,31,33,37]

GPIO.setup(chan_list, GPIO.OUT, initial=GPIO.LOW)

def set_random_bulbs():
	number_of_bulbs = randint(0,7)
	chans = list(chan_list)
	for bulbs in range(0, number_of_bulbs):
		bulb = randint(0, len(chans) - 1)
		toggle_bulb(chans[bulb])
		chans.remove(chans[bulb])

def toggle_bulb(bulb):
	GPIO.output(bulb, not GPIO.input(bulb))

def get_random_bulb():
	return chan_list[randint(0,7)]

##Program starts here	
print("Running...")

try:
	set_random_bulbs()
	while True:
		time.sleep(5)
		set_random_bulbs()
		#toggle_bulb(get_random_bulb())
except KeyboardInterrupt:
	GPIO.cleanup()
	time.sleep(0.2)
	print("""
kthxbai!""")
	exit(0)