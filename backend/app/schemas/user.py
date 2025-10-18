from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


# User schemas
class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.CLINICIAN
    first_name: str
    last_name: str
    specialty: Optional[str] = None
    license_number: Optional[str] = None


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    specialty: Optional[str] = None
    phone: Optional[str] = None
    preferences: Optional[dict] = None


class UserProfileResponse(BaseModel):
    """User profile response schema."""
    id: int
    first_name: str
    last_name: str
    specialty: Optional[str]
    license_number: Optional[str]
    phone: Optional[str]
    preferences: Optional[dict]

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    """User response schema."""
    id: int
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime]
    profile: Optional[UserProfileResponse]

    class Config:
        from_attributes = True


# Token schemas
class Token(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""
    user_id: Optional[int] = None
    email: Optional[str] = None
