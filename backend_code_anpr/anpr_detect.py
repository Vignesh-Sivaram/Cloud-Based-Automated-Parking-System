# anpr/anpr_detect.py
import boto3
import re
import sys
from datetime import datetime
from math import ceil

# helper modules (must match signatures described below)
from database.dynamodb_insert import save_entry, close_entry
from database.dynamodb_fetch import get_active_record  # <-- ensure this name
from sms.send_sms_email import send_entry_sms, send_exit_sms
from slots.slot_manager import allocate_slot, free_slot

BUCKET_NAME = "smart-parking-vehicle-images"


def extract_number_plate(text_list):
    pattern = r"[A-Z]{2}\d{1,2}[A-Z]{1,2}\d{3,4}"

    # Remove country identifier if present
    cleaned = [t for t in text_list if t.upper() != "IND"]

    combined = "".join(t.replace(" ", "").upper() for t in cleaned)

    match = re.search(pattern, combined)
    if match:
        return match.group()

    return None


def calculate_bill(minutes):
    """
    Example billing:
     - First hour flat ₹40
     - After first hour: ₹1 per minute
     - Minimum ₹20
    """
    if minutes <= 60:
        return 40
    return 40 + (minutes - 60)


def detect_vehicle(image_name, prompt_for_mobile=True, default_mobile="+919043723379"):
    rek = boto3.client("rekognition")
    print(f"\n🔍 Processing image: {image_name}")

    try:
        response = rek.detect_text(
            Image={"S3Object": {"Bucket": BUCKET_NAME, "Name": image_name}}
        )
    except Exception as e:
        print("❌ Rekognition failed:", e)
        return

    text_detections = response.get("TextDetections", [])
    detected_lines = [it["DetectedText"] for it in text_detections if it.get("Type") == "LINE"]
    print("📄 Raw Detected Lines:", detected_lines)

    number_plate = extract_number_plate(detected_lines)
    if not number_plate:
        print("\n❌ No valid number plate detected. Try again with a clearer image.")
        return

    print(f"\n🚗 Number Plate Detected: {number_plate}")

    # Check DB for active (parked) record
    try:
        existing = get_active_record(number_plate)
    except Exception as e:
        print("❌ Error reading DB:", e)
        return

    if existing is None:
        # ENTRY
        print("\n🟢 Vehicle is ENTERING...")

        slot = allocate_slot()
        if slot is None:
            print("❌ Parking Full! Cannot assign slot.")
            return

        # Determine mobile: prefer operator prompt (real projects use a UI or registry)
        mobile = None
        if prompt_for_mobile:
            inp = input("Enter owner's mobile in E.164 format (+91...) or press Enter to use default: ").strip()
            mobile = inp if inp else default_mobile
        else:
            mobile = default_mobile

        # Current timestamp as entry time
        entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save entry (save_entry creates entry_time inside)
        try:
            save_entry(number_plate, image_name, slot, mobile)
            # CALL SNS ENTRY SMS
            send_entry_sms(number_plate, slot, entry_time, mobile)
        except Exception as e:
            print("❌ Error saving entry:", e)
            # rollback slot reservation
            free_slot(slot)
            return

        print(f"\n✅ ENTRY recorded: {number_plate} → Slot {slot}")
        return


    else:
        # EXIT
        print("\n🔵 Vehicle is EXITING...")

        entry_time_str = existing.get("entry_time")
        if not entry_time_str:
            print("❌ Stored record has no entry_time. Aborting.")
            return

        entry_time = datetime.strptime(entry_time_str, "%Y-%m-%d %H:%M:%S")
        exit_time = datetime.now()
        duration_minutes = int((exit_time - entry_time).total_seconds() // 60)
        amount = calculate_bill(duration_minutes)
        exit_time_str = exit_time.strftime("%Y-%m-%d %H:%M:%S")

        try:
            close_entry(number_plate, exit_time_str, duration_minutes, amount)
        except Exception as e:
            print("❌ Error updating DB for exit:", e)
            return

        # free slot (best-effort)
        slot_id = existing.get("slot")
        if slot_id:
            freed = free_slot(slot_id)
            if not freed:
                print("⚠ Could not free slot:", slot_id)

        # send SMS to owner (mobile fetched from DB inside close_entry or use existing['mobile'])
        mobile = existing.get("mobile")
        if mobile:
            try:
                send_exit_sms(number_plate, duration_minutes, amount, mobile)
            except Exception as e:
                print("⚠ Failed to send exit SMS:", e)

        print(f"\n✅ EXIT completed for {number_plate}")
        print(f"⏱ Duration: {duration_minutes} min")
        print(f"💰 Bill: ₹{amount}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python anpr_detect.py <image_name>")
        sys.exit(1)
    detect_vehicle(sys.argv[1])
