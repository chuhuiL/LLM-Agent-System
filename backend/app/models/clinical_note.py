from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.database import Base


class NoteStatus(str, enum.Enum):
    """Status of clinical note."""
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    SIGNED = "signed"
    AMENDED = "amended"


class ClinicalNote(Base):
    """Clinical note/documentation record."""

    __tablename__ = "clinical_notes"

    id = Column(Integer, primary_key=True, index=True)
    encounter_id = Column(Integer, nullable=False, index=True)
    template_id = Column(Integer, nullable=True, index=True)
    status = Column(SQLEnum(NoteStatus), nullable=False, default=NoteStatus.DRAFT)
    title = Column(String(255), nullable=True)
    version = Column(Integer, default=1, nullable=False)
    created_by_id = Column(Integer, nullable=False, index=True)
    signed_by_id = Column(Integer, nullable=True)
    signed_at = Column(DateTime(timezone=True), nullable=True)
    fhir_document_reference_id = Column(String(100), nullable=True)  # FHIR DocumentReference ID
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    encounter = relationship("Encounter", back_populates="clinical_notes")
    template = relationship("Template", back_populates="clinical_notes")
    created_by_user = relationship("User", back_populates="clinical_notes", foreign_keys=[created_by_id])
    sections = relationship("NoteSection", back_populates="note", cascade="all, delete-orphan")
    versions = relationship("NoteVersion", back_populates="note", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ClinicalNote(id={self.id}, encounter_id={self.encounter_id}, status={self.status}, version={self.version})>"


class NoteSection(Base):
    """Individual section of a clinical note."""

    __tablename__ = "note_sections"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, nullable=False, index=True)
    section_type = Column(String(100), nullable=False)  # e.g., "subjective", "objective", "assessment", "plan"
    section_title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    order = Column(Integer, nullable=False, default=0)
    agent_generated = Column(Boolean, default=False, nullable=False)
    reviewed = Column(Boolean, default=False, nullable=False)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    metadata = Column(JSON, nullable=True)  # ICD codes, SNOMED codes, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    note = relationship("ClinicalNote", back_populates="sections")

    def __repr__(self):
        return f"<NoteSection(id={self.id}, note_id={self.note_id}, type={self.section_type})>"


class NoteVersion(Base):
    """Version history for clinical notes."""

    __tablename__ = "note_versions"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, nullable=False, index=True)
    version = Column(Integer, nullable=False)
    content_json = Column(JSON, nullable=False)  # Complete note structure
    created_by_id = Column(Integer, nullable=False)
    change_description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    note = relationship("ClinicalNote", back_populates="versions")

    def __repr__(self):
        return f"<NoteVersion(id={self.id}, note_id={self.note_id}, version={self.version})>"
