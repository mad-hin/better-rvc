import os
import shutil
import cv2
from tqdm import tqdm


class Inference:
    def __init__(self):
        pass

    def inference_bulk_image(self, input_folder_path: str, threshold: float = 0.25, separation: bool = True,
                             output_folder_path: str = "output") -> None:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        left_folder = output_folder_path + '/professor_left'
        middle_folder = output_folder_path + '/professor_middle'
        right_folder = output_folder_path + '/professor_right'

        os.makedirs(left_folder, exist_ok=True)
        os.makedirs(middle_folder, exist_ok=True)
        os.makedirs(right_folder, exist_ok=True)

        # Threshold for "near" left or right (25% of image width)
        threshold = 0.25

        image_files = [f for f in os.listdir(input_folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        for image_name in tqdm(image_files, desc="Processing images"):
            image_path = os.path.join(input_folder_path, image_name)
            image = cv2.imread(image_path)
            if image is None:
                continue

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            img_width = image.shape[1]

            for (x, y, w, h) in faces:
                face_center_x = x + w / 2

                if face_center_x < img_width * threshold:
                    if separation:
                        shutil.move(image_path, os.path.join(left_folder, image_name))
                    print(f"{image_name}: Moved to professor_left")
                elif face_center_x > img_width * (1 - threshold):
                    if separation:
                        shutil.move(image_path, os.path.join(right_folder, image_name))
                    print(f"{image_name}: Moved to professor_right")
                else:
                    if separation:
                        shutil.move(image_path, os.path.join(middle_folder, image_name))
                    print(f"{image_name}: Moved to professor_middle")
                break  # Process only the first detected face to avoid multiple moves


    def inference_single_image(self, image_path: str, threshold: float = 0.25, show_img = True) -> None:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not load image at {image_path}")
            return

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        img_width = image.shape[1]

        for (x, y, w, h) in faces:
            face_center_x = x + w / 2
            if face_center_x < img_width * threshold:
                position = "LEFT"
            elif face_center_x > img_width * (1 - threshold):
                position = "RIGHT"
            else:
                position = "MIDDLE"

            print(f"Professor's face is on the {position} side of {os.path.basename(image_path)}")
            print(f"Bounding square coordinates: Top-left ({x}, {y}), Bottom-right ({x + w}, {y + h})")

            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.putText(image, f"Position: {position}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            break  # Process only the first detected face

        # If no faces are detected
        if len(faces) == 0:
            print(f"No faces detected in {os.path.basename(image_path)}")

        if show_img:
            cv2.imshow('Face Detection', image)
            cv2.waitKey(0)  # Wait for any key press to close the window
            cv2.destroyAllWindows()


    def inference_real_time(self, threshold: float = 0.25):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        cap = cv2.VideoCapture(0)  # 0 is the default webcam

        if not cap.isOpened():
            print("Error: Could not open webcam")
            exit()

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            img_width = frame.shape[1]

            for (x, y, w, h) in faces:
                face_center_x = x + w / 2
                position = ""
                if face_center_x < img_width * threshold:
                    position = "LEFT"
                elif face_center_x > img_width * (1 - threshold):
                    position = "RIGHT"
                else:
                    position = "MIDDLE"

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                cv2.putText(frame, f"Position: {position}", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                break

            cv2.imwrite('Webcam - Face Position.png', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


    def no_inference(self):
        cap = cv2.VideoCapture(0)
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            cv2.imshow('Webcam - Face Position', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

Inference().no_inference()

