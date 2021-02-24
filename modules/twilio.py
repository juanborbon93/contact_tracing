from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
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
    return 

def reply_to_text(message:str):
    response = MessagingResponse()
    msg = response.message(message)
    return response


