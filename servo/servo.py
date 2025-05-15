import RPi.GPIO as GPIO
from time import sleep

def ServoSetup(pin = 19):
	"""
	Initializes and sets up a GPIO pin for servo control using PWM.

	Args:
		pin (int, optional): The GPIO pin number to use (BOARD numbering). Defaults to 7.

	Returns:
		PWM: An instance of the GPIO.PWM class configured for the specified pin at 50Hz.

	Notes:
		- If the GPIO is already in use, the setup step is skipped and a message is printed.
		- The PWM signal is started with a 0% duty cycle.
	"""
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.OUT)

	pwm = GPIO.PWM(pin, 50)
	pwm.start(7)  # Neutral position
	return pwm

def SetAngle(angle, pwm, pin = 19):
	"""
	Sets the angle of a servo motor using PWM.

	Args:
		angle (float): The desired angle to set the servo to (in degrees).
		pwm (PWM): The PWM instance controlling the servo.
		pin (int, optional): The GPIO pin number connected to the servo. Defaults to 7.

	Note:
		Assumes that the GPIO and PWM have been properly initialized before calling this function.
	"""
	duty = 2.0 + ((angle + 90) / 180.0) * (12.0 - 2.0)
	pwm.ChangeDutyCycle(duty)
	print(f"Setting angle to {angle} degrees, duty cycle: {duty}")
	sleep(0.5)  # Let servo reach position
	pwm.ChangeDutyCycle(0)  # Stop sending signal to reduce jitter

def ServoCleanup(pwm):
	"""
	Stops the given PWM instance and cleans up the GPIO resources.

	Args:
		pwm: The PWM instance to stop.
	
	Note:
		This function should be called to properly release hardware resources
		when the servo is no longer needed.

		You SHOULD call this function at the end of your program to ensure the GPIO Port are free.
	"""
	pwm.stop()
	GPIO.cleanup()
