from pathlib import Path


from sqlmodel import create_engine, Session
from model import HealthcareProfessional, Patient

DATABASE_URL = "sqlite:///" + str(Path(__file__).parent / "db" / "florence.db")

if __name__ == "__main__":
    engine = create_engine(DATABASE_URL)

    # Create a Session
    session = Session(engine)

    # Insert a HealthcareProfessional
    new_healthcare_professional = HealthcareProfessional(email="jannic.holzer@gmail.com")
    session.add(new_healthcare_professional)
    session.commit()  # commit to get the id of new_healthcare_professional

    # Insert a Patient linked to the HealthcareProfessional
    new_patient = Patient(
        first_name="John",
        last_name="Doe",
        patient_number="4857773456",
        healthcare_professional_id=new_healthcare_professional.id
    )
    session.add(new_patient)
    session.commit()
