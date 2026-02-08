from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel


class UserBase(SQLModel):
    """Base model for User with common fields."""
    email: str = Field(unique=True, nullable=False, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)


class User(UserBase, table=True):
    """User model for the database."""
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user", cascade_delete=True)
    threads: list["Thread"] = Relationship(back_populates="user", cascade_delete=True)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserRead(UserBase):
    """User model for reading (without sensitive data)."""
    id: UUID
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    """User model for creation."""
    password: str


class UserUpdate(BaseModel):
    """User model for updates."""
    name: Optional[str] = None
    email: Optional[str] = None