import re
from pathlib import Path

from decouple import config
from fastapi import Depends, FastAPI, Form
from sqlmodel import Session, create_engine, select
from twilio.rest import Client as TwilioClient

from model import NextOfKin, Patient, init_db
from query import ChatSession
from seed_db import seed_database
from send_message import WhatsAppMessageSender

ACCOUNT_SID = config("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = config("TWILIO_NUMBER")
DESTINATION_NUMBER = config("DESTINATION_NUMBER")
OPENAI_API_KEY = config("OPENAI_API_KEY")

twilio_client = TwilioClient(ACCOUNT_SID, AUTH_TOKEN)
sender = WhatsAppMessageSender(twilio_client, TWILIO_NUMBER)
chat_session = ChatSession(patient_number="4857773456")

app = FastAPI()

DATABASE_URL = "sqlite:///" + str(Path(__file__).parent / "db" / "florence.db")
ENGINE = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
FORM_REGEX = r"Patient First Name: (.+)\nPatient Last Name: (.+)\nPatient Date of Birth: (\d{2}\/\d{2}\/\d{4})"


@app.on_event("startup")
def on_startup():
    init_db(DATABASE_URL)
    try:
        seed_database(DATABASE_URL)
    except:
        pass


def get_session():
    with Session(ENGINE) as session:
        yield session


@app.post("/message")
async def reply(
    Body: str = Form(...),
    From: str = Form(...),
    session: Session = Depends(get_session),
):
    print(f"received message {Body} from {From}")
    from_number = From.replace("whatsapp:", "")
    next_of_kin = get_next_of_kin(session, from_number)

    # reset command for testing only for demo purposes
    if Body.lower() == "!reset" and next_of_kin:
        next_of_kin.is_authenticated = False
        session.add(next_of_kin)
        session.commit()
        return ""

    if next_of_kin and next_of_kin.is_authenticated:
        llm_response = chat_session.query(Body)
        sender.send_message(next_of_kin.phone_number, llm_response)
        return ""

    form_match = re.match(FORM_REGEX, Body)

    if not form_match:
        send_unauthenticated_message(from_number)
        return ""

    parsed_form = parse_form_message(form_match)
    patient = get_patient(session, parsed_form["first_name"], parsed_form["last_name"])
    print(f"Found Patient {patient}")

    if not patient or not next_of_kin or patient.next_of_kin_id != next_of_kin.id:
        sender.send_message(
            from_number,
            "I'm sorry I didn't find any patients matching the information you provided. Please try again. 🙁",
        )
        return ""

    mark_next_of_kin_as_authenticated(session, next_of_kin.phone_number)
    sender.send_message(
        from_number,
        "The information you provided matches our records. I can now share information about your loved one's care. 👍",
    )

    return ""


def get_next_of_kin(session: Session, phone_number: str) -> NextOfKin | None:
    query = select(NextOfKin).where(NextOfKin.phone_number == phone_number)
    return session.exec(query).first()


def get_patient(session: Session, first_name: str, last_name: str) -> Patient | None:
    query = select(Patient).where(
        (Patient.first_name == first_name) & (Patient.last_name == last_name)
    )
    return session.exec(query).first()


def mark_next_of_kin_as_authenticated(session: Session, phone_number: str):
    next_of_kin = get_next_of_kin(session, phone_number)
    if not next_of_kin:
        return

    next_of_kin.is_authenticated = True
    session.add(next_of_kin)
    session.commit()


def parse_form_message(form_match) -> dict:
    return {
        "first_name": form_match.group(1),
        "last_name": form_match.group(2),
        "date_of_birth": form_match.group(3),
    }


def send_unauthenticated_message(to_number: str):
    message = """Hi there! I'm Florence 👋 👩🏻‍⚕️

I'm here to help you stay up to date with your loved one's care during their time in hospital 🏥.

In order to get started, I need to know some details about the patient you are inquiring about 📝.

Please reply with the following information in the exact format presented below:

Patient First Name: <patient first name>
Patient Last Name: <patient last name>
Patient Date of Birth: <patient date of birth in the format DD/MM/YYYY>"""

    sender.send_message(
        to_number,
        message,
    )
