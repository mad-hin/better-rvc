import servo

pwm = servo.ServoSetup()
servo.SetAngle(10, pwm)
print("Current angle: 15")
# servo.SetAngle(0, pwm)
servo.SetAngle(0, pwm)
print("Current angle: 0")
# servo.SetAngle(-5, pwm)
servo.SetAngle(-10, pwm) 
print("Current angle: -15")
servo.ServoCleanup(pwm)
