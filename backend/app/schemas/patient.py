from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime


class PatientBase(BaseModel):
    """Base patient schema."""
    mrn: str = Field(..., description="Medical Record Number")
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    date_of_birth: date
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[dict] = None


class PatientCreate(PatientBase):
    """Schema for creating a new patient."""
    demographics: Optional[dict] = None


class PatientUpdate(BaseModel):
    """Schema for updating patient information."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[dict] = None
    demographics: Optional[dict] = None


class PatientResponse(PatientBase):
    """Patient response schema."""
    id: int
    fhir_id: Optional[str]
    demographics: Optional[dict]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class PatientConsentCreate(BaseModel):
    """Schema for creating patient consent."""
    patient_id: int
    consent_type: str
    granted: bool
    notes: Optional[str] = None


class PatientConsentResponse(BaseModel):
    """Patient consent response schema."""
    id: int
    patient_id: int
    consent_type: str
    granted: bool
    granted_at: Optional[datetime]
    revoked_at: Optional[datetime]
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
