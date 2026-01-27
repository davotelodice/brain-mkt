"""Authentication API endpoints."""
import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.database import get_db
from ..db.models import MarketingPasswordResetToken, MarketingProject, MarketingUser
from ..schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    RequestPasswordResetRequest,
    RequestPasswordResetResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
)
from ..utils.jwt import create_access_token
from ..utils.password import hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)) -> RegisterResponse:
    """Register new user.

    Args:
        request: Registration data
        db: Database session

    Returns:
        Created user info

    Raises:
        HTTPException: If email already exists in project or project not found
    """
    # 1. Verify project exists
    project_result = await db.execute(
        select(MarketingProject).where(MarketingProject.id == request.project_id)
    )
    if not project_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Project not found")

    # 2. Check if email already exists in this project
    existing_user = await db.execute(
        select(MarketingUser).where(
            MarketingUser.email == request.email,
            MarketingUser.project_id == request.project_id
        )
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered in this project")

    # 3. Hash password
    hashed_password = hash_password(request.password)

    # 4. Create user
    new_user = MarketingUser(
        email=request.email,
        password_hash=hashed_password,
        full_name=request.full_name,
        project_id=request.project_id
    )
    db.add(new_user)
    await db.flush()

    return RegisterResponse(
        id=new_user.id,
        email=new_user.email,
        full_name=new_user.full_name,
        project_id=new_user.project_id
    )


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)) -> LoginResponse:
    """Login user.

    Args:
        request: Login credentials
        db: Database session

    Returns:
        JWT token and user info

    Raises:
        HTTPException: If credentials are invalid
    """
    # 1. Find user by email + project_id
    result = await db.execute(
        select(MarketingUser).where(
            MarketingUser.email == request.email,
            MarketingUser.project_id == request.project_id
        )
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # 2. Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # 3. Update last_login
    user.last_login = datetime.utcnow()
    await db.flush()

    # 4. Generate JWT
    token = create_access_token({
        "user_id": str(user.id),
        "email": user.email,
        "project_id": str(user.project_id)
    })

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user={
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "project_id": str(user.project_id)
        }
    )


@router.post("/request-password-reset", response_model=RequestPasswordResetResponse)
async def request_password_reset(
    request: RequestPasswordResetRequest,
    db: AsyncSession = Depends(get_db)
) -> RequestPasswordResetResponse:
    """Request password reset token.

    Args:
        request: Email and project_id
        db: Database session

    Returns:
        Reset token (in production, send via email)

    Raises:
        HTTPException: If user not found
    """
    # 1. Find user
    result = await db.execute(
        select(MarketingUser).where(
            MarketingUser.email == request.email,
            MarketingUser.project_id == request.project_id
        )
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Generate unique token
    reset_token = str(uuid.uuid4())

    # 3. Save token (expires in 1 hour)
    token_record = MarketingPasswordResetToken(
        user_id=user.id,
        project_id=user.project_id,
        token=reset_token,
        expires_at=datetime.utcnow() + timedelta(hours=1)
    )
    db.add(token_record)
    await db.flush()

    # TODO: In production, send email with reset link
    return RequestPasswordResetResponse(
        message="Password reset token generated",
        token=reset_token
    )


@router.post("/reset-password", response_model=ResetPasswordResponse)
async def reset_password(
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db)
) -> ResetPasswordResponse:
    """Reset password using token.

    Args:
        request: Token and new password
        db: Database session

    Returns:
        Success message

    Raises:
        HTTPException: If token is invalid, used, or expired
    """
    # 1. Find token
    result = await db.execute(
        select(MarketingPasswordResetToken).where(
            MarketingPasswordResetToken.token == request.token
        )
    )
    token_record = result.scalar_one_or_none()

    if not token_record:
        raise HTTPException(status_code=404, detail="Invalid token")

    if token_record.used:
        raise HTTPException(status_code=400, detail="Token already used")

    if token_record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")

    # 2. Find user
    user_result = await db.execute(
        select(MarketingUser).where(MarketingUser.id == token_record.user_id)
    )
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 3. Update password
    user.password_hash = hash_password(request.new_password)

    # 4. Mark token as used
    token_record.used = True
    await db.flush()

    return ResetPasswordResponse(message="Password reset successful")
