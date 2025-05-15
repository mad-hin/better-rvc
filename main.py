import servo.servo as servo
from cv_recognition.inference_all import Inference
import cv2
import LoRa.uart_test as uart
import time


if __name__ == "__main__":
    try:
        pwm = servo.ServoSetup()
        angle = 0
        cv_override = False
        # The main loop to control the servo
        servo.SetAngle(angle, pwm)
        print(f"Current angle: {angle}")
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(99)  # 0 is the default webcam
        infer = Inference()
        uart.start_serial_thread()

        light_off_start = None  # Track when light turns off
        not_exit = True  # Flag to indicate if the program should exit

        while True:
            pos = infer.inference_real_time(cap, face_cascade, threshold= 0.25)
            print(pos)
            channel = uart.get_closer_to_channel()
            print(f"Current closer_to_channel: {channel}")
            light = uart.get_light_status()
            print(f"Current light status: {light}")
            
            # Check the channel and light status to determine the servo position
            if (light == 1):
                light_off_start = None  # Reset counter if light is on
                not_exit = True  # Set flag to indicate the program should not exit
                if (pos == "NO FACE" and not cv_override):
                    if channel == -1:
                        angle += 25
                        if angle > 90:
                            angle = 90
                        servo.SetAngle(angle, pwm)
                        print(f"Current angle: {angle}")
                    elif channel == 1:
                        angle -= 25
                        if angle < -90:
                            angle = -90
                        servo.SetAngle(angle, pwm)
                        print(f"Current angle: {angle}")
                    else:
                        pass # No action needed
                
                if (pos == "LEFT"):
                    cv_override = True
                    angle += 10
                    if angle > 90:
                        angle = 90
                    servo.SetAngle(angle, pwm)
                    print(f"Current angle: {angle}")
                elif (pos == "RIGHT"):
                    cv_override = True
                    angle -= 10
                    if angle < -90:
                        angle = -90
                    servo.SetAngle(angle, pwm)
                    print(f"Current angle: {angle}")
                else:
                    cv_override = True
                    print(f"Current angle: {angle}")
                # time.sleep(1)
            else:
                if light_off_start is None:
                    light_off_start = time.time()
                else:
                    elapsed = time.time() - light_off_start
                    print(f"Light has been off for {int(elapsed)} seconds.")
                    if elapsed >= 30:
                        print("Light has been off for 30 seconds!")
                        # Place your 30s action here
                        light_off_start = time.time()  # Reset if you want repeated actions every 30s
                        servo.SetAngle(0, pwm)
                        cv_override = False

    except KeyboardInterrupt:
        # Handle the case when the user interrupts the program
        print("Interrupted by user. Cleaning up...")
        servo.ServoCleanup(pwm)
        cap.release()
        cv2.destroyAllWindows()