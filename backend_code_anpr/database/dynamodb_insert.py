# database/dynamodb_insert.py
import boto3
from datetime import datetime

ddb = boto3.resource("dynamodb")
entries_table = ddb.Table("ParkingEntries")

def save_entry(number_plate, image_file, slot_number, mobile="+91XXXXXXXXXX"):
    """
    Save a new entry record and send entry SMS.
    """
    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item = {
        "number_plate": number_plate,
        "entry_time": entry_time,
        "slot": slot_number,
        "image_file": image_file,
        "mobile": mobile,
        "status": "parked"
    }
    entries_table.put_item(Item=item)
    print("✅ Entry stored in DynamoDB:", number_plate)

def close_entry(number_plate, exit_time_str, duration_minutes, amount):
    """
    Update the existing record with exit details and send exit SMS.
    Expects that the entry exists.
    """
    # First fetch record to get mobile
    resp = entries_table.get_item(Key={"number_plate": number_plate})
    item = resp.get("Item")
    if not item:
        print("No entry found for", number_plate)
        return

    mobile = item.get("mobile")

    # Update record
    entries_table.update_item(
        Key={"number_plate": number_plate},
        UpdateExpression="""
            SET exit_time = :e,
                duration_minutes = :d,
                bill_amount = :b,
                #st = :s
        """,
        ExpressionAttributeNames={
            "#st": "status"
        },
        ExpressionAttributeValues={
            ":e": exit_time_str,
            ":d": duration_minutes,
            ":b": amount,
            ":s": "exited"
        }
    )
    print("✅ Exit updated in DynamoDB for", number_plate)


