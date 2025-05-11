# Face Position Detection

This project provides a Python implementation for detecting the position of a person's face (left, middle, or right) in images or real-time webcam feed using OpenCV's Haar cascade classifier. The `Inference` class includes three methods to process images in bulk, analyze a single image, or perform real-time detection via webcam.

## Features
- **Bulk Image Processing**: Processes a folder of images, classifies face positions, and optionally moves images to folders (`professor_left`, `professor_middle`, `professor_right`).
- **Single Image Analysis**: Detects the face position in a single image, prints the position and bounding box coordinates, and displays the annotated image.
- **Real-Time Webcam Detection**: Detects face positions in real-time using a webcam, showing the position and bounding box on the video feed.

## Requirements
- Python 3.6+
- Libraries:
  - OpenCV (`opencv-python`)
  - TQDM (for progress bar in bulk processing)
- Install dependencies:
  ```bash
  pip install opencv-python tqdm
  ```
- A webcam (for real-time detection).
- Images in `.png`, `.jpg`, or `.jpeg` format (for bulk/single image processing).

## File Structure
- `inference.py`: Main Python script containing the `Inference` class with the three detection methods.
- `faces/`: Input folder for bulk image processing (create this folder and add images).
- `output/`: Output folder for bulk processing (automatically created with subfolders `professor_left`, `professor_middle`, `professor_right`).

## Usage

### 1. Bulk Image Processing
Processes all images in a specified folder and sorts them based on face position.

```python
from inference import Inference

infer = Inference()
infer.inference_bulk_image(
    input_folder_path="faces",
    threshold=0.25,
    separation=True,
    output_folder_path="output"
)
```

- **Parameters**:
  - `input_folder_path`: Path to the folder containing images.
  - `threshold`: Fraction of image width to define "left" or "right" (default: 0.25, i.e., 25% from edges).
  - `separation`: If `True`, moves images to `professor_left`, `professor_middle`, or `professor_right` folders.
  - `output_folder_path`: Path for output folders (default: "output").
- **Output**: Prints the position for each image and moves images to corresponding folders if `separation=True`.

### 2. Single Image Analysis
Analyzes a single image, prints the face position and bounding box coordinates, and displays the image with annotations.

```python
from inference import Inference

infer = Inference()
infer.inference_single_image(
    image_path="faces/image.jpg",
    threshold=0.25,
    show_img=True
)
```

- **Parameters**:
  - `image_path`: Path to the input image.
  - `threshold`: Fraction of image width to define "left" or "right" (default: 0.25).
  - `show_img`: If `True`, displays the image with a bounding box and position label.
- **Output**: Prints the position (e.g., "Professor's face is on the LEFT side") and coordinates (e.g., "Top-left (50, 100), Bottom-right (150, 200)"). Shows the annotated image if `show_img=True`.

### 3. Real-Time Webcam Detection
Detects face positions in real-time using the webcam.

```python
from inference import Inference

infer = Inference()
infer.inference_real_time(threshold=0.25)
```

- **Parameters**:
  - `threshold`: Fraction of frame width to define "left" or "right" (default: 0.25).
- **Output**: Displays a webcam feed with a green bounding box around the first detected face and a label (e.g., "Position: LEFT"). Press `q` to exit.

## Notes
- **Face Detection**: Uses OpenCV's Haar cascade classifier (`haarcascade_frontalface_default.xml`), which is CPU-based and included with OpenCV.
- **Accuracy**: Haar cascades may miss faces in poor lighting or at odd angles. For better accuracy, consider MTCNN or YOLOv8-face (not implemented here).
- **Threshold**: The default `threshold=0.25` means "left" and "right" are within 25% of the image/frame edges. Adjust as needed.
- **Performance**: For large image sets or real-time processing, performance may be limited on low-end CPUs. GPU-accelerated models (e.g., MTCNN with CUDA) can improve speed.
- **Multiple Faces**: All methods process only the first detected face per image/frame. Modify the code to handle multiple faces if needed.

## Troubleshooting
- **Webcam Issues**: Ensure the webcam is connected and not in use by another application. Try `cv2.VideoCapture(1)` if `cv2.VideoCapture(0)` fails.
- **Image Loading Errors**: Verify image paths and ensure files are valid `.png`, `.jpg`, or `.jpeg`.
- **No Faces Detected**: Adjust `scaleFactor` (e.g., 1.05) or `minNeighbors` (e.g., 3) in the `detectMultiScale` call for better detection, but this may increase false positives.
- **Slow Performance**: Resize images (e.g., to 640x480) or use a GPU-based model for faster processing.

## License
This project is licensed under the MIT License.
