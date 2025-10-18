from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Text, JSON, Boolean
from sqlalchemy.sql import func
import enum

from app.db.database import Base


class FHIRResourceType(str, enum.Enum):
    """FHIR resource types."""
    PATIENT = "Patient"
    ENCOUNTER = "Encounter"
    DOCUMENT_REFERENCE = "DocumentReference"
    OBSERVATION = "Observation"
    CONDITION = "Condition"
    MEDICATION_REQUEST = "MedicationRequest"
    PRACTITIONER = "Practitioner"


class SyncOperation(str, enum.Enum):
    """FHIR synchronization operations."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    SEARCH = "search"


class SyncStatus(str, enum.Enum):
    """FHIR synchronization status."""
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"


class FHIRMapping(Base):
    """Mapping between local records and FHIR resources."""

    __tablename__ = "fhir_mappings"

    id = Column(Integer, primary_key=True, index=True)
    local_table = Column(String(100), nullable=False, index=True)  # e.g., "patients", "encounters"
    local_id = Column(Integer, nullable=False, index=True)
    resource_type = Column(SQLEnum(FHIRResourceType), nullable=False)
    fhir_id = Column(String(100), nullable=False, index=True)  # FHIR resource ID
    fhir_version_id = Column(String(100), nullable=True)  # FHIR resource version
    last_synced = Column(DateTime(timezone=True), nullable=True)
    sync_metadata = Column(JSON, nullable=True)  # Additional sync information
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<FHIRMapping(local={self.local_table}:{self.local_id}, fhir={self.resource_type}:{self.fhir_id})>"


class FHIRSyncLog(Base):
    """Log of FHIR synchronization operations."""

    __tablename__ = "fhir_sync_logs"

    id = Column(Integer, primary_key=True, index=True)
    resource_type = Column(SQLEnum(FHIRResourceType), nullable=False, index=True)
    resource_id = Column(String(100), nullable=True)
    operation = Column(SQLEnum(SyncOperation), nullable=False)
    status = Column(SQLEnum(SyncStatus), nullable=False)
    request_data = Column(JSON, nullable=True)  # Request payload
    response_data = Column(JSON, nullable=True)  # Response from FHIR server
    error_message = Column(Text, nullable=True)
    duration_ms = Column(Integer, nullable=True)  # Operation duration in milliseconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<FHIRSyncLog(id={self.id}, operation={self.operation}, status={self.status})>"
