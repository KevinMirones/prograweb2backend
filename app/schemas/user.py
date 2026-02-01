from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime, text
from datetime import datetime, timezone

class UserBase(SQLModel):
    email: str = Field(sa_column=Column("email_user", String(255), unique=True, nullable=False))
    is_active: bool = Field(default=True, sa_column=Column("is_active_user", Boolean, default=True))
    mfa_enabled: bool = Field(default=False, sa_column=Column("mfa_enabled_user", Boolean, default=False))

class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, sa_column=Column("id_user", Integer, primary_key=True))
    hashed_password: str = Field(sa_column=Column("password_user", String(255), nullable=False))
    mfa_secret: Optional[str] = Field(default=None, sa_column=Column("mfa_secret_user", String(255), nullable=True))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column("created_at_user", DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

class UserLogin(SQLModel):
    email: str
    password: str
    mfa_code: Optional[str] = None
