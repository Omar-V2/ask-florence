from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session


class NextOfKin(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    phone_number: str
    is_authenticated: bool = False


class Patient(SQLModel, table=True):
    patient_number: str = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    next_of_kin_id: Optional[int] = Field(default=None, foreign_key="nextofkin.id")
    healthcare_professional_id: int = Field(foreign_key="healthcareprofessional.id")


class HealthcareProfessional(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str


def init_db(database_url: str):
    engine = create_engine(database_url)
    with Session(engine) as session:
        session.execute("PRAGMA foreign_keys=on")
        session.commit()
        SQLModel.metadata.create_all(engine)
