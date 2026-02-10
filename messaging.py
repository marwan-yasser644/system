from twilio.rest import Client
from flask import current_app

def get_twilio_client():
    sid = current_app.config["TWILIO_ACCOUNT_SID"]
    token = current_app.config["TWILIO_AUTH_TOKEN"]
    return Client(sid, token)

def send_attendance_sms(student_name, parent_phone, date_str, center_name="Center"):
    if not (current_app.config["TWILIO_ACCOUNT_SID"] and current_app.config["TWILIO_AUTH_TOKEN"] and current_app.config["TWILIO_FROM_NUMBER"]):
        return  
    client = get_twilio_client()
    body = (
        f"Dear Parent,\n\n"
        f"The attendance of the student: {student_name} "
        f"has been recorded for today's lesson on {date_str}.\n\n"
        f"Best regards,\n{center_name} Administration"
    )
    client.messages.create(
        body=body,
        from_=current_app.config["TWILIO_FROM_NUMBER"],
        to=parent_phone
    )
