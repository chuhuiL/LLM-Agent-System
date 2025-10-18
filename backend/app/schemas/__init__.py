"""
Pydantic schemas for API request/response validation.
"""

from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserUpdate,
    UserResponse,
    UserProfileResponse,
    Token,
    TokenData
)
from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientResponse,
    PatientConsentCreate,
    PatientConsentResponse
)

__all__ = [
    # User schemas
    "UserCreate",
    "UserLogin",
    "UserUpdate",
    "UserResponse",
    "UserProfileResponse",
    "Token",
    "TokenData",
    # Patient schemas
    "PatientCreate",
    "PatientUpdate",
    "PatientResponse",
    "PatientConsentCreate",
    "PatientConsentResponse",
]
