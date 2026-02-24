# sms/send_sms.py
import boto3

sns = boto3.client("sns", region_name="ap-south-1")

def send_sms(phone_number, message):
    #phone_number: E.164 format string, e.g. '+919876543210'
    #message: string
    
    try:
        resp = sns.publish(PhoneNumber=phone_number, Message=message)
        # resp contains 'MessageId' on success
        return resp
    except Exception as e:
        print("Error sending SMS:", e)
        return None

def send_entry_sms(number_plate, slot, entry_time, phone):
    msg = (
        f"Your Entry Confirmed: {number_plate}\n"
        f"You can park at Slot: {slot}\n"
        f"Entry Time: {entry_time}"
    )
    return send_sms(phone, msg)

def send_exit_sms(number_plate, duration_min, amount, phone):
    msg = (
        f"You are Exiting: {number_plate}\n"
        f"Duration stayed: {duration_min} min\n"
        f"Pay your Parking Fee: ₹{amount}\n"
        f"====Thank you!===="
    )
    return send_sms(phone, msg)

# 🔴 Replace this with your SNS Email Topic ARN
"""EMAIL_TOPIC_ARN = "arn:aws:sns:ap-south-1:010419877614:smart-parking-email-topic"

def send_email(subject, message):
    #Sends email using Amazon SNS topic
    try:
        resp = sns.publish(
            TopicArn=EMAIL_TOPIC_ARN,
            Subject=subject,
            Message=message
        )
        return resp
    except Exception as e:
        print("Error sending Email:", e)
        return None


def send_entry_sms(number_plate, slot, entry_time):
    #ENTRY email
    #(Function name kept same to avoid changing rest of project)
    msg = (
        f"🚗 Parking Entry Confirmed\n\n"
        f"Your Vehicle Number : {number_plate}\n"
        f"You are Allocated Slot : {slot}\n"
        f"Entry Time     : {entry_time}\n\n"
        f"===Welcome==="
    )

    return send_email(
        subject="Parking Entry Confirmation",
        message=msg
    )


def send_exit_sms(number_plate, duration_min, amount):
    #EXIT email
    msg = (
        f"🚘 Parking Exit Details\n\n"
        f"Your Vehicle Number : {number_plate}\n"
        f"Duration Stayed: {duration_min} minutes\n"
        f"Pay your Parking Fee    : ₹{amount}\n\n"
        f"==== Thank You ===="
    )

    return send_email(
        subject="Parking Exit & Billing Details",
        message=msg
    )
"""