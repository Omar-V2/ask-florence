from decouple import config
from twilio.rest import Client as TwilioClient

from send_message import WhatsAppMessageSender

if __name__ == "__main__":
    account_sid = config("TWILIO_ACCOUNT_SID")
    auth_token = config("TWILIO_AUTH_TOKEN")
    twilio_number = config("TWILIO_NUMBER")
    destination_number = config("DESTINATION_NUMBER")

    twilio_client = TwilioClient(account_sid, auth_token)
    sender = WhatsAppMessageSender(twilio_client, twilio_number)
    sender.send_message(destination_number, "Hello from Twilio!")
