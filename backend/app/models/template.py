from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.database import Base


class TemplateType(str, enum.Enum):
    """Types of clinical note templates."""
    SOAP = "soap"  # Subjective, Objective, Assessment, Plan
    HP = "hp"  # History & Physical
    PROGRESS = "progress"  # Progress Note
    DISCHARGE = "discharge"  # Discharge Summary
    CONSULT = "consult"  # Consultation Note
    CUSTOM = "custom"  # Custom template


class Template(Base):
    """Clinical note template definition."""

    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    template_type = Column(SQLEnum(TemplateType), nullable=False)
    description = Column(Text, nullable=True)
    structure_json = Column(JSON, nullable=False)  # Template structure definition
    is_active = Column(Boolean, default=True, nullable=False)
    is_system = Column(Boolean, default=False, nullable=False)  # System vs user-created
    created_by_id = Column(Integer, nullable=True)
    specialty = Column(String(200), nullable=True)  # Target specialty (e.g., "Cardiology")
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    sections = relationship("TemplateSection", back_populates="template", cascade="all, delete-orphan")
    clinical_notes = relationship("ClinicalNote", back_populates="template")

    def __repr__(self):
        return f"<Template(id={self.id}, name={self.name}, type={self.template_type})>"


class FieldType(str, enum.Enum):
    """Field types for template sections."""
    TEXT = "text"
    TEXTAREA = "textarea"
    RICH_TEXT = "rich_text"
    SELECT = "select"
    MULTISELECT = "multiselect"
    CHECKBOX = "checkbox"
    DATE = "date"
    NUMBER = "number"
    ICD_CODE = "icd_code"
    SNOMED_CODE = "snomed_code"
    MEDICATION = "medication"


class TemplateSection(Base):
    """Section definition within a template."""

    __tablename__ = "template_sections"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, nullable=False, index=True)
    section_name = Column(String(255), nullable=False)
    section_type = Column(String(100), nullable=False)  # e.g., "subjective", "assessment"
    description = Column(Text, nullable=True)
    order = Column(Integer, nullable=False, default=0)
    required = Column(Boolean, default=False, nullable=False)
    field_schema = Column(JSON, nullable=False)  # Field definitions for this section
    ai_prompt = Column(Text, nullable=True)  # Custom prompt for AI to fill this section
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    template = relationship("Template", back_populates="sections")

    def __repr__(self):
        return f"<TemplateSection(id={self.id}, template_id={self.template_id}, name={self.section_name})>"
