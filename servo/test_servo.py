import servo

pwm = servo.ServoSetup()
servo.SetAngle(45, pwm)
print("Current angle: 45")
# servo.SetAngle(0, pwm)
servo.SetAngle(0, pwm)
print("Current angle: 0")
# servo.SetAngle(-5, pwm)
servo.SetAngle(-45, pwm) 
print("Current angle: -15")
servo.ServoCleanup(pwm)
