import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

print(GPIO.getmode())

chan_list = [36,32,26,24,22,18,16,8,7,11,13,15,29,31,33,37]

GPIO.setup(chan_list, GPIO.OUT, initial=GPIO.HIGH)

print("Testing...")

try:
	while True:

			#GPIO.output(11, GPIO.LOW)
			GPIO.output(chan_list, GPIO.LOW)
			time.sleep(.3)
			GPIO.output(chan_list, GPIO.HIGH)
			time.sleep(.4)
except KeyboardInterrupt:
	GPIO.cleanup()
	time.sleep(0.2)
	print("""
kthxbai!""")
	exit(0)



