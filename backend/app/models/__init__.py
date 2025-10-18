"""
SQLAlchemy models for the Clinical Documentation Platform.
"""

from app.models.user import User, UserProfile, Session, UserRole
from app.models.patient import Patient, PatientConsent
from app.models.encounter import Encounter, ConsultationInput, EncounterType, EncounterStatus, InputType
from app.models.clinical_note import ClinicalNote, NoteSection, NoteVersion, NoteStatus
from app.models.template import Template, TemplateSection, TemplateType, FieldType
from app.models.agent import (
    AgentTask,
    AgentExecution,
    HumanReview,
    ReflectionLog,
    TaskStatus,
    TaskType,
    ReviewAction
)
from app.models.fhir import FHIRMapping, FHIRSyncLog, FHIRResourceType, SyncOperation, SyncStatus
from app.models.audit import AuditTrail

__all__ = [
    # User models
    "User",
    "UserProfile",
    "Session",
    "UserRole",
    # Patient models
    "Patient",
    "PatientConsent",
    # Encounter models
    "Encounter",
    "ConsultationInput",
    "EncounterType",
    "EncounterStatus",
    "InputType",
    # Clinical note models
    "ClinicalNote",
    "NoteSection",
    "NoteVersion",
    "NoteStatus",
    # Template models
    "Template",
    "TemplateSection",
    "TemplateType",
    "FieldType",
    # Agent models
    "AgentTask",
    "AgentExecution",
    "HumanReview",
    "ReflectionLog",
    "TaskStatus",
    "TaskType",
    "ReviewAction",
    # FHIR models
    "FHIRMapping",
    "FHIRSyncLog",
    "FHIRResourceType",
    "SyncOperation",
    "SyncStatus",
    # Audit model
    "AuditTrail",
]
