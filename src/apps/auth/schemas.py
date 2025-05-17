from typing import Literal, Union

from pydantic import BaseModel, Field, ConfigDict, EmailStr

from src.apps.user.enums import UserRole


class TokenSchema(BaseModel):
    access_token: str | None
    refresh_token: str | None
    token_type: Literal["Bearer"] = "Bearer"


class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(examples=["password"])


class AccessTokenPayloadSchema(BaseModel):
    user_id: int = Field(alias="id")
    role: UserRole

    model_config = ConfigDict(use_enum_values=True, from_attributes=True)


class RefreshTokenPayloadSchema(BaseModel):
    user_id: int
    jti: str
    fingerprint: str

    model_config = ConfigDict(from_attributes=True)


class StudentInviteSchema(BaseModel):
    email: EmailStr
    group_id: int
    role: Literal[UserRole.STUDENT]


class TeacherInviteSchema(BaseModel):
    email: EmailStr
    department_id: int
    role: Literal[UserRole.TEACHER]


class UniversityInviteSchema(BaseModel):
    email: EmailStr
    role: Literal[UserRole.UNIVERSITY_ADMIN]


class InviteSchema(BaseModel):
    register_url: str
    invite_body: Union[StudentInviteSchema, TeacherInviteSchema]

    model_config = ConfigDict(use_enum_values=True, from_attributes=True)
