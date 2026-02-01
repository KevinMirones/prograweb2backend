from datetime import timedelta
from typing import Any
import secrets
import string

from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlmodel import Session, select
from app.core.database import get_db
from app.schemas.user import User, UserCreate, UserRead, UserLogin
from app.core import security
from app.services.email_service import send_mfa_code
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

def generate_verification_code(length=6):
    return ''.join(secrets.choice(string.digits) for _ in range(length))

@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.email == user_in.email)).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user = User(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        is_active=user_in.is_active,
        mfa_enabled=user_in.mfa_enabled
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = db.exec(select(User).where(User.email == login_data.email)).first()
    if not user or not security.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # MFA Logic
    if user.mfa_enabled:
        if not login_data.mfa_code:
            # Generate and send code
            code = generate_verification_code()
            user.mfa_secret = code # In production store this with expiration!
            db.add(user)
            db.commit()
            
            # Send Email
            await send_mfa_code(user.email, code)
            
            return {"message": "MFA code sent", "mfa_required": True}
        else:
            # Verify code
            if user.mfa_secret != login_data.mfa_code:
                 raise HTTPException(status_code=400, detail="Invalid MFA Code")
            # Clear code? Or leave it until next login? Better clear.
            user.mfa_secret = None
            db.add(user)
            db.commit()

    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "mfa_required": False
    }
