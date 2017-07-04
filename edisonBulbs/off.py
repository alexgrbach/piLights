import time
import RPi.GPIO as GPIO
from random import randint

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

chan_list = [7,11,13,15,29,31,33,37]

GPIO.setup(chan_list, GPIO.OUT, initial=GPIO.LOW)

print("off")

try:
	while True:
		time.sleep(100)
except KeyboardInterrupt:
	GPIO.cleanup()
	time.sleep(0.2)
	print("""
kthxbai!""")
	exit(0)



