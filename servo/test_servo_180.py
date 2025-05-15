import RPi.GPIO as GPIO
import time

# setup the GPIO pin for the servo
servo_pin = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin,GPIO.OUT)

# setup PWM process
pwm = GPIO.PWM(servo_pin,50) # 50 Hz (20 ms PWM period)

pwm.start(7) # start PWM by rotating to 90 degrees

def angle_to_duty_cycle(angle):
    # Maps -90 to 90 degrees to 2.0-12.0 duty cycle
    return 2.0 + ((angle + 90) / 180.0) * (12.0 - 2.0)

for ii in range(0,2):
    # pwm.start(angle_to_duty_cycle(0))
    pwm.ChangeDutyCycle(angle_to_duty_cycle(0)) # rotate to 0 degrees
    time.sleep(1)
    # pwm.ChangeDutyCycle(0) # rotate to 90 degrees
    # pwm.stop() # stops the pwm on 19
    # time.sleep(1)
    # pwm.start(angle_to_duty_cycle(5))
    pwm.ChangeDutyCycle(angle_to_duty_cycle(70)) # rotate to 180 degrees
    time.sleep(1)
    # pwm.ChangeDutyCycle(0) # rotate to 90 degrees
    # pwm.stop() # stops the pwm on 19

    # pwm.start(angle_to_duty_cycle(0))
    # # pwm.ChangeDutyCycle(angle_to_duty_cycle(0)) # rotate to 90 degrees
    # time.sleep(1)
    # pwm.stop() # stops the pwm on 19

pwm.ChangeDutyCycle(0) # this prevents jitter
pwm.stop() # stops the pwm on 13
GPIO.cleanup() # good practice when finished using a pin