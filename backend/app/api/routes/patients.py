from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.patient import Patient, PatientConsent
from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientResponse,
    PatientConsentCreate,
    PatientConsentResponse
)
from app.services.audit import log_audit

router = APIRouter()


@router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient_data: PatientCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new patient record.

    Args:
        patient_data: Patient information
        current_user: Current authenticated user
        db: Database session

    Returns:
        Created patient information

    Raises:
        HTTPException: If MRN already exists
    """
    # Check if patient with MRN already exists
    existing_patient = db.query(Patient).filter(Patient.mrn == patient_data.mrn).first()
    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient with this MRN already exists"
        )

    # Create patient
    patient = Patient(**patient_data.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)

    # Log audit
    log_audit(db, current_user.id, "create", "patient", patient.id, f"Patient created: {patient.full_name}")

    return patient


@router.get("", response_model=List[PatientResponse])
async def list_patients(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, description="Search by name or MRN"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    List patients with optional search.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        search: Optional search term
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of patients
    """
    query = db.query(Patient).filter(Patient.is_active == True)

    # Apply search filter
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Patient.first_name.ilike(search_pattern)) |
            (Patient.last_name.ilike(search_pattern)) |
            (Patient.mrn.ilike(search_pattern))
        )

    patients = query.offset(skip).limit(limit).all()
    return patients


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get patient by ID.

    Args:
        patient_id: Patient ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Patient information

    Raises:
        HTTPException: If patient not found
    """
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.is_active == True
    ).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Log audit
    log_audit(db, current_user.id, "read", "patient", patient_id, f"Patient viewed: {patient.full_name}")

    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: int,
    patient_update: PatientUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update patient information.

    Args:
        patient_id: Patient ID
        patient_update: Updated patient data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated patient information

    Raises:
        HTTPException: If patient not found
    """
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.is_active == True
    ).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Update patient fields
    update_data = patient_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)

    # Log audit
    log_audit(db, current_user.id, "update", "patient", patient_id, f"Patient updated: {patient.full_name}")

    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
    patient_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Soft delete patient (deactivate).

    Args:
        patient_id: Patient ID
        current_user: Current authenticated user
        db: Database session

    Raises:
        HTTPException: If patient not found
    """
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Soft delete
    patient.is_active = False
    db.commit()

    # Log audit
    log_audit(db, current_user.id, "delete", "patient", patient_id, f"Patient deactivated: {patient.full_name}")


@router.post("/{patient_id}/consents", response_model=PatientConsentResponse, status_code=status.HTTP_201_CREATED)
async def create_patient_consent(
    patient_id: int,
    consent_data: PatientConsentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create patient consent record.

    Args:
        patient_id: Patient ID
        consent_data: Consent information
        current_user: Current authenticated user
        db: Database session

    Returns:
        Created consent record

    Raises:
        HTTPException: If patient not found
    """
    # Verify patient exists
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Create consent
    consent = PatientConsent(**consent_data.model_dump())
    db.add(consent)
    db.commit()
    db.refresh(consent)

    # Log audit
    log_audit(db, current_user.id, "create", "patient_consent", consent.id,
              f"Consent created for patient {patient_id}: {consent_data.consent_type}")

    return consent
