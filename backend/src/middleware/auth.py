"""Authentication middleware and dependencies."""
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.database import get_db
from ..db.models import MarketingUser
from ..utils.jwt import decode_access_token

security = HTTPBearer(auto_error=False)  # ✅ No error if missing (try cookie first)


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> MarketingUser:
    """Get current authenticated user from JWT token.

    ✅ GOTCHA 10: Supports both cookie (httpOnly) and Bearer token (for API clients).

    Priority:
    1. Cookie `auth_token` (httpOnly, used by frontend)
    2. Header `Authorization: Bearer` (for API clients)

    Args:
        request: FastAPI request (to read cookies)
        credentials: HTTP Bearer token (optional)
        db: Database session

    Returns:
        Current user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    # ✅ Priority 1: Try cookie (httpOnly for frontend)
    token = request.cookies.get("auth_token")

    # ✅ Priority 2: Try Bearer token (for API clients)
    if not token and credentials:
        token = credentials.credentials

    # No token found
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    payload = decode_access_token(token)

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    # Get user from database
    result = await db.execute(
        select(MarketingUser).where(MarketingUser.id == UUID(user_id))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
