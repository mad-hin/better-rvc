import servo
import time 

pwm = servo.ServoSetup()
servo.SetAngle(45, pwm)
print("Current angle: 45")
# time.sleep(0.1)
# servo.SetAngle(0, pwm)
servo.SetAngle(0, pwm)
print("Current angle: 0")
# time.sleep(0.1)
# servo.SetAngle(-5, pwm)
servo.SetAngle(-45, pwm) 
print("Current angle: -45")
# time.sleep(0.1)
servo.ServoCleanup(pwm)
