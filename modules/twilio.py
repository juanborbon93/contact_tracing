from twilio.rest import Client
import os

account = os.environ.get("TWILIO_ACCOUNT")
token = os.environ.get("TWILIO_TOKEN")
messaging_service_sid = os.environ.get("MESSAGING_SERVICE_SID")

client = Client(account,token)

def send_text(message:str,number:str):
    message = client.messages.create(
        body=message,
        messaging_service_sid = messaging_service_sid,
        to=number)


