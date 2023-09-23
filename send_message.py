import logging

from twilio.rest import Client as TwilioClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WhatsAppMessageSender:
    def __init__(self, twilio_client: TwilioClient, twilio_number: str) -> None:
        self.twilio_client = twilio_client
        self.twilio_number = twilio_number

    def send_message(self, to_number: str, body_text: str) -> None:
        try:
            message = self.twilio_client.messages.create(
                from_=f"whatsapp:{self.twilio_number}",
                body=body_text,
                to=f"whatsapp:{to_number}",
            )
            logger.info(f"Message sent to {to_number}: {message.body}")
            print(f"Message sent to {to_number}: {message.body}")
        except Exception as e:
            logger.error(f"Error sending message to {to_number}: {e}")
