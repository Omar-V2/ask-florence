from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session

from pathlib import Path


DATABASE_URL = "sqlite:///" + str(Path(__file__).parent / "db" / "florence.db")


class NextOfKin(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    phone_number: str


class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    ehr: str
    next_of_kin_id: Optional[int] = Field(default=None, foreign_key="nextofkin.id")
    healthcare_professional_id: int = Field(foreign_key="healthcareprofessional.id")


class HealthcareProfessional(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str


def init_db():
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        session.execute("PRAGMA foreign_keys=on")
        session.commit()
        SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
