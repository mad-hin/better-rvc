import servo.servo as servo
# from cv_recognition.inference_all import Inference

if __name__ == "__main__":
    try:
        pwm = servo.ServoSetup()
        angle = 0
        # The main loop to control the servo
        while True:
            # Read the current angle from the servo
            servo.SetAngle(angle, pwm)
            print(f"Current angle: {angle}")

    except KeyboardInterrupt:
        # Handle the case when the user interrupts the program
        print("Interrupted by user. Cleaning up...")
        servo.ServoCleanup(pwm)