import cv2
import os
import shutil
from tqdm import tqdm


def detect_and_move_faces(input_dir="frames", output_dir="faces"):
    # Create output directory for images with faces if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the pre-trained Haar Cascade Classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        print("Error: Could not load Haar Cascade Classifier")
        return

    # Get list of image files
    image_files = [f for f in os.listdir(input_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Process each image with a progress bar
    for filename in tqdm(image_files, desc="Processing images"):
        # Read the image
        img_path = os.path.join(input_dir, filename)
        img = cv2.imread(img_path)
        if img is None:
            print(f"Warning: Could not read image {filename}")
            continue

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # If faces are detected, move the image to the faces directory
        if len(faces) > 0:
            dest_path = os.path.join(output_dir, filename)
            shutil.move(img_path, dest_path)
            print(f"Moved {filename} to {output_dir} (faces detected: {len(faces)})")
        else:
            print(f"No faces detected in {filename}, leaving in {input_dir}")

    print("Face detection and sorting completed")


if __name__ == "__main__":
    # Example usage
    input_directory = "frames"  # Directory containing extracted frames
    faces_directory = "faces"  # Directory for images with faces
    detect_and_move_faces(input_directory, faces_directory)
