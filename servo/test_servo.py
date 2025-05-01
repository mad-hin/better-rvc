import servo

pwm = servo.ServoSetup()
servo.SetAngle(5, pwm)
# servo.SetAngle(0, pwm)
servo.SetAngle(0, pwm)
servo.ServoCleanup(pwm)
