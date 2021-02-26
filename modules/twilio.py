from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os

account = os.environ.get("TWILIO_ACCOUNT")
token = os.environ.get("TWILIO_TOKEN")
app_phone_number = os.environ.get("APP_PHONE_NUMBER")

client = Client(account,token)

def send_text(message:str,number:str):
    message = client.messages.create(
        body=message,
        from_ = app_phone_number,
        to=number)
    return 

def reply_to_text(message:str):
    response = MessagingResponse()
    msg = response.message(message)
    return response


