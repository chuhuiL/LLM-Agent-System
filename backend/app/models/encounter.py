from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.database import Base


class EncounterType(str, enum.Enum):
    """Types of clinical encounters."""
    OUTPATIENT = "outpatient"
    INPATIENT = "inpatient"
    EMERGENCY = "emergency"
    VIRTUAL = "virtual"
    FOLLOWUP = "followup"


class EncounterStatus(str, enum.Enum):
    """Status of clinical encounter."""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Encounter(Base):
    """Clinical encounter (consultation) record."""

    __tablename__ = "encounters"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, nullable=False, index=True)
    clinician_id = Column(Integer, nullable=False, index=True)
    encounter_type = Column(SQLEnum(EncounterType), nullable=False)
    status = Column(SQLEnum(EncounterStatus), nullable=False, default=EncounterStatus.SCHEDULED)
    encounter_date = Column(DateTime(timezone=True), nullable=False)
    chief_complaint = Column(Text, nullable=True)
    fhir_id = Column(String(100), unique=True, nullable=True)  # FHIR Encounter resource ID
    metadata = Column(JSON, nullable=True)  # Additional encounter data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    patient = relationship("Patient", back_populates="encounters")
    consultation_inputs = relationship("ConsultationInput", back_populates="encounter", cascade="all, delete-orphan")
    clinical_notes = relationship("ClinicalNote", back_populates="encounter", cascade="all, delete-orphan")
    agent_tasks = relationship("AgentTask", back_populates="encounter", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Encounter(id={self.id}, patient_id={self.patient_id}, type={self.encounter_type}, status={self.status})>"


class InputType(str, enum.Enum):
    """Types of consultation input."""
    AUDIO = "audio"
    TRANSCRIPT = "transcript"
    TEXT = "text"
    VIDEO = "video"


class ConsultationInput(Base):
    """Input data for consultation (audio, transcript, etc.)."""

    __tablename__ = "consultation_inputs"

    id = Column(Integer, primary_key=True, index=True)
    encounter_id = Column(Integer, nullable=False, index=True)
    input_type = Column(SQLEnum(InputType), nullable=False)
    content = Column(Text, nullable=True)  # For text/transcript
    file_url = Column(String(500), nullable=True)  # For audio/video files
    file_size = Column(Integer, nullable=True)  # File size in bytes
    duration = Column(Integer, nullable=True)  # Duration in seconds (for audio/video)
    metadata = Column(JSON, nullable=True)  # Additional metadata (speaker labels, etc.)
    processed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    encounter = relationship("Encounter", back_populates="consultation_inputs")

    def __repr__(self):
        return f"<ConsultationInput(id={self.id}, encounter_id={self.encounter_id}, type={self.input_type})>"
