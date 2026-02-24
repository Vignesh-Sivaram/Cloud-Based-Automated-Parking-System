from capture_upload import capture_and_upload
from anpr_detect import detect_vehicle

if __name__ == "__main__":
    image_name = capture_and_upload()
    if image_name:
        detect_vehicle(image_name)
