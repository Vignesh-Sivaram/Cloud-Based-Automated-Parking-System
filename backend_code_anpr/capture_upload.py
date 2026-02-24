import cv2
import boto3
from datetime import datetime

def capture_and_upload():
    # Capture image
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()

    if not ret:
        print("❌ Failed to capture image")
        return None

    # Unique filename using timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_name = f"vehicle_{timestamp}.jpg"

    cv2.imwrite(image_name, frame)

    # Upload to S3
    s3 = boto3.client("s3")
    s3.upload_file(image_name, "smart-parking-vehicle-images", image_name)

    print(f"✅ Image uploaded successfully: {image_name}")
    return image_name


# Allow standalone execution (important)
if __name__ == "__main__":
    capture_and_upload()
