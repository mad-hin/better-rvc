import servo.servo as servo
from cv_recognition.inference_all import Inference
import cv2
import LoRa.uart_test as uart
import time


if __name__ == "__main__":
    try:
        pwm = servo.ServoSetup()
        angle = 0
        # The main loop to control the servo
        servo.SetAngle(angle, pwm)
        print(f"Current angle: {angle}")
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)  # 0 is the default webcam
        infer = Inference()
        uart.start_serial_thread()

        while True:
            pos = infer.inference_real_time(cap, face_cascade, threshold= 0.25)
            print(pos)
            channel = uart.get_closer_to_channel()
            print(f"Current closer_to_channel: {channel}")
            light = uart.get_light_status()
            print(f"Current light status: {light}")
            
            # Check the channel and light status to determine the servo position
            if (pos == "LEFT"):
                angle += 5
                if angle > 90:
                    angle = 90
                servo.SetAngle(angle, pwm)
                print(f"Current angle: {angle}")
            elif (pos == "RIGHT"):
                angle -= 5
                if angle < -90:
                    angle = -90
                servo.SetAngle(angle, pwm)
                print(f"Current angle: {angle}")
            else:
                pass
            # time.sleep(1)

    except KeyboardInterrupt:
        # Handle the case when the user interrupts the program
        print("Interrupted by user. Cleaning up...")
        servo.ServoCleanup(pwm)
        cap.release()
        cv2.destroyAllWindows()