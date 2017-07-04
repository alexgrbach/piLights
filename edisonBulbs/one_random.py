import time
import RPi.GPIO as GPIO
from random import randint

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

print(GPIO.getmode())

chan_list = [7,11,13,15,29,31,33,37]

GPIO.setup(chan_list, GPIO.OUT, initial=GPIO.LOW)

print("Testing...")

try:
	while True:
		chan = chan_list[randint(0,7)]
		GPIO.output(chan, GPIO.HIGH)
		time.sleep(3)
		GPIO.output(chan, GPIO.LOW) 
except KeyboardInterrupt:
	GPIO.cleanup()
	time.sleep(0.2)
	print("""
kthxbai!""")
	exit(0)



