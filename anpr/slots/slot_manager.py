# slots/slot_manager.py
import boto3
from boto3.dynamodb.conditions import Attr
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
slots_table = dynamodb.Table("ParkingSlots")

def allocate_slot():
    """
    Find a free slot and reserve it atomically using conditional update.
    Returns the reserved slot_id (string) or None if no slot available.
    """
    # Simple approach: scan for free slots (small table). For large scale use GSI / query patterns.
    resp = slots_table.scan(
        FilterExpression=Attr("is_free").eq(True),
        ProjectionExpression="slot_id"
    )
    items = resp.get("Items", [])
    if not items:
        return None

    # Try to reserve first candidate atomically
    for it in items:
        slot_id = it["slot_id"]
        try:
            slots_table.update_item(
                Key={"slot_id": slot_id},
                UpdateExpression="SET is_free = :f, reserved_at = :t",
                ConditionExpression=Attr("is_free").eq(True),
                ExpressionAttributeValues={
                    ":f": False,
                    ":t": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                },
            )
            # Reserved successfully
            return slot_id
        except Exception:
            # Condition failed or other error, try next slot
            continue
    return None

def free_slot(slot_id):
    """
    Mark a slot as free. Returns True if updated.
    """
    try:
        slots_table.update_item(
            Key={"slot_id": slot_id},
            UpdateExpression="SET is_free = :f REMOVE reserved_at",
            ExpressionAttributeValues={":f": True}
        )
        return True
    except Exception as e:
        print("Error freeing slot:", e)
        return False
