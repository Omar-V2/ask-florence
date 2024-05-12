from sqlmodel import Session, create_engine
from model import HealthcareProfessional, Patient, NextOfKin


def seed_database(database_url: str):
    engine = create_engine(database_url)

    session = Session(engine)

    # Insert a HealthcareProfessional
    new_healthcare_professional = HealthcareProfessional(
        email="jannic.holzer@gmail.com"
    )
    session.add(new_healthcare_professional)
    session.commit()  # commit to get the id of new_healthcare_professional

    # Insert a Patient linked to the HealthcareProfessional
    john_doe = Patient(
        first_name="John",
        last_name="Doe",
        patient_number="4857773456",
        healthcare_professional_id=new_healthcare_professional.id,
    )

    # Insert a next of kin for John
    jane_doe = NextOfKin(
        id=1,
        first_name="Jane",
        last_name="Doe",
        phone_number="+447500513650",
        is_authenticated=False,
    )

    john_doe.next_of_kin_id = jane_doe.id

    session.add(john_doe)
    session.add(jane_doe)

    # Insert a new different Patient linked to the same HealthcareProfessional
    sally_smith = Patient(
        first_name="John",
        last_name="Smith",
        patient_number="4857773457",
        healthcare_professional_id=new_healthcare_professional.id,
    )

    # Insert a next of kin for Sally
    jack_smith = NextOfKin(
        id=2,
        first_name="Sally",
        last_name="Smith",
        phone_number="+447960852993",
        is_authenticated=False,
    )

    sally_smith.next_of_kin_id = jack_smith.id

    session.add(sally_smith)
    session.add(jack_smith)

    session.commit()
