import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT) # Set the pwm signal wire to PIN 7

pwm=GPIO.PWM(7, 50)
pwm.start(0)

def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(7, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(7, False)
	pwm.ChangeDutyCycle(0)

pwm.stop()
GPIO.cleanup()
