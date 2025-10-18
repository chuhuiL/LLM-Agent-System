from sqlalchemy import Column, Integer, String, Date, DateTime, JSON, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import date

from app.db.database import Base


class Patient(Base):
    """Patient demographic information."""

    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    mrn = Column(String(50), unique=True, index=True, nullable=False)  # Medical Record Number
    fhir_id = Column(String(100), unique=True, nullable=True, index=True)  # FHIR Patient resource ID
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(JSON, nullable=True)  # Street, city, state, zip, country
    demographics = Column(JSON, nullable=True)  # Additional demographic data
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    encounters = relationship("Encounter", back_populates="patient", cascade="all, delete-orphan")
    consents = relationship("PatientConsent", back_populates="patient", cascade="all, delete-orphan")

    @property
    def full_name(self) -> str:
        """Get patient's full name."""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int:
        """Calculate patient's age."""
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def __repr__(self):
        return f"<Patient(id={self.id}, mrn={self.mrn}, name={self.full_name})>"


class PatientConsent(Base):
    """Patient consent records for various purposes."""

    __tablename__ = "patient_consents"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, nullable=False, index=True)
    consent_type = Column(String(100), nullable=False)  # e.g., "data_sharing", "ai_processing"
    granted = Column(Boolean, nullable=False)
    granted_at = Column(DateTime(timezone=True), nullable=True)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    patient = relationship("Patient", back_populates="consents")

    def __repr__(self):
        return f"<PatientConsent(patient_id={self.patient_id}, type={self.consent_type}, granted={self.granted})>"
