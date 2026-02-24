import boto3
from boto3.dynamodb.conditions import Key

# Connect to DynamoDB
ddb = boto3.resource('dynamodb')
table = ddb.Table("ParkingEntries")

# ------------------------------------------------
# CHECK IF VEHICLE ALREADY EXISTS IN THE DATABASE
# ------------------------------------------------
def check_vehicle(number_plate):
    """
    Returns:
        dict  -> if vehicle exists (parked or exited record)
        None  -> if vehicle does not exist
    """

    response = table.get_item(Key={"number_plate": number_plate})

    if "Item" in response:
        return response["Item"]
    return None


# ------------------------------------------------
# GET ONLY ACTIVE PARKED VEHICLE RECORD
# (status = 'parked')
# ------------------------------------------------
def get_active_record(number_plate):
    """
    Returns only active-parking record (status = parked)

    Used during EXIT detection.
    """

    record = check_vehicle(number_plate)
    if record and record.get("status") == "parked":
        return record

    return None


# ------------------------------------------------
# GET LIST OF ALL PARKED VEHICLES
# ------------------------------------------------
def list_all_parked():
    """
    Returns a list of all currently parked vehicles.
    """

    response = table.scan(
        FilterExpression=Key("status").eq("parked")
    )
    return response.get("Items", [])


# ------------------------------------------------
# GET LIST OF ALL VEHICLES (ENTRIES + EXITS)
# ------------------------------------------------
def list_all_entries():
    """
    Returns every vehicle record in the table.
    """

    response = table.scan()
    return response.get("Items", [])
