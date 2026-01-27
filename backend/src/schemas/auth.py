"""Pydantic schemas for authentication."""
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    """User registration request."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Password (min 8 chars)")
    full_name: str | None = Field(None, description="User full name")
    project_id: UUID = Field(..., description="Project to join")

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class RegisterResponse(BaseModel):
    """User registration response."""
    id: UUID
    email: str
    full_name: str | None
    project_id: UUID


class LoginRequest(BaseModel):
    """User login request."""
    email: EmailStr
    password: str
    project_id: UUID


class LoginResponse(BaseModel):
    """User login response."""
    access_token: str
    token_type: str = "bearer"
    user: dict  # {id, email, full_name, project_id}


class RequestPasswordResetRequest(BaseModel):
    """Request password reset."""
    email: EmailStr
    project_id: UUID


class RequestPasswordResetResponse(BaseModel):
    """Password reset request response."""
    message: str
    token: str  # In production, send via email link


class ResetPasswordRequest(BaseModel):
    """Reset password with token."""
    token: str
    new_password: str = Field(..., min_length=8)

    @field_validator('new_password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class ResetPasswordResponse(BaseModel):
    """Reset password response."""
    message: str
