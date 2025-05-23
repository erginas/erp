from typing import Optional

from pydantic import EmailStr
from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field


class Users(SQLModel, table=True):
    __tablename__ = "USERS"  # Oracle'da büyük harf kullanılıyor olabilir

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, max_length=255)
    hashed_password: str
    full_name: Optional[str] = None
    is_active: Optional[bool] = Field(default=True)
    is_superuser: Optional[bool] = Field(default=False)
    is_staff: Optional[bool] = Field(default=False)
    role: Optional[str] = Field(
        sa_column=Column("ROLE", String(50), nullable=True)
    )


# Shared properties


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    role: Optional[str] = Field(default="viewer", max_length=50)  # ✅


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int | None = Field(default=None, primary_key=True)


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None
    role: str | None = None  # ✅ Eklendi


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
