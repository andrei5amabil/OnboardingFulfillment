import os
import jwt
from typing import List
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from dotenv import load_dotenv
import sys
from pathlib import Path
from src.db import supabase
import logging

logger = logging.getLogger("uvicorn.error")

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path, override=True)

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

security = HTTPBearer()

class CurrentUser(BaseModel):
    user_id: str
    email: str
    role: str
    employee_id: str | None = None

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> CurrentUser:
    token = credentials.credentials
    try:
        user_response = supabase.auth.get_user(token)
        auth_user = user_response.user

        if not auth_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired session token."
            )
        user_id = auth_user.id
        email = auth_user.email or ""

    except Exception as e:
        logger.error(f"❌ Supabase Auth verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}"
        )

    res = (
        supabase.table("users")
        .select("role, is_active, employee_id")
        .eq("user_id", user_id)
        .single()
        .execute()
    )
    user_data = res.data

    if not user_data or not user_data.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive or not found in users table."
        )

    return CurrentUser(
        user_id=user_id,
        email=email,
        role=user_data["role"],
        employee_id=user_data.get("employee_id")
    )

class RequireRoles:
    """Dependency factory enforcing specific roles. 'admin' always has full access."""
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if user.role == "admin" or user.role in self.allowed_roles:
            return user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied. Requires one of: {self.allowed_roles}"
        )