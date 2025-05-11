import cv2
import os


def extract_frames(video_path, k, output_dir="frames"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file")
        return

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    print(f"Total frames: {frame_count}, FPS: {fps}")

    current_frame = 0
    saved_frame_count = 0

    while True:
        # Read frame
        ret, frame = cap.read()
        if not ret:
            break

        if current_frame % k == 0:
            height = frame.shape[0]
            crop_height = int(height * 2 / 3)
            cropped_frame = frame[0:crop_height, :]
            output_path = os.path.join(output_dir, f"frame_{saved_frame_count:06d}.jpg")
            # Save cropped frame as JPEG
            cv2.imwrite(output_path, cropped_frame)
            saved_frame_count += 1

        current_frame += 1

    cap.release()
    print(f"Saved {saved_frame_count} frames to {output_dir}")


if __name__ == "__main__":
    # Example usage
    video_file = "2025-05-11 02-03-39.mp4"  # Replace with your video path
    frame_interval = 10  # Extract every 10th frame
    extract_frames(video_file, frame_interval)
