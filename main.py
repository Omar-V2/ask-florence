from decouple import config
from fastapi import FastAPI, Form
from twilio.rest import Client as TwilioClient

from query import ChatSession
from send_message import WhatsAppMessageSender

account_sid = config("TWILIO_ACCOUNT_SID")
auth_token = config("TWILIO_AUTH_TOKEN")
twilio_number = config("TWILIO_NUMBER")
destination_number = config("DESTINATION_NUMBER")
openai_api_key = config("OPENAI_API_KEY")

twilio_client = TwilioClient(account_sid, auth_token)
sender = WhatsAppMessageSender(twilio_client, twilio_number)
session = ChatSession(patient_id=1)

app = FastAPI()


@app.post("/message")
async def reply(Body: str = Form()):
    print(f"received message {Body}")
    llm_response = session.query(Body)
    print(llm_response)
    sender.send_message(destination_number, llm_response)
    return ""
