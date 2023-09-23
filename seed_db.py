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
    new_patient = Patient(
        first_name="John",
        last_name="Doe",
        patient_number="4857773456",
        healthcare_professional_id=new_healthcare_professional.id,
    )

    # Insert a next of kin
    new_next_of_kin = NextOfKin(
        id=1,
        first_name="Jane",
        last_name="Doe",
        phone_number="+447500513650",
        is_authenticated=False,
    )

    new_patient.next_of_kin_id = new_next_of_kin.id

    session.add(new_patient)
    session.add(new_next_of_kin)
    session.commit()
