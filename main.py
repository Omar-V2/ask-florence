from decouple import config
from fastapi import FastAPI, Form
from twilio.rest import Client as TwilioClient

from send_message import WhatsAppMessageSender

account_sid = config("TWILIO_ACCOUNT_SID")
auth_token = config("TWILIO_AUTH_TOKEN")
twilio_number = config("TWILIO_NUMBER")
destination_number = config("DESTINATION_NUMBER")

twilio_client = TwilioClient(account_sid, auth_token)
sender = WhatsAppMessageSender(twilio_client, twilio_number)

app = FastAPI()


@app.post("/message")
async def reply(Body: str = Form()):
    echo_message = f"You said: {Body}"
    sender.send_message(destination_number, echo_message)
    return ""
