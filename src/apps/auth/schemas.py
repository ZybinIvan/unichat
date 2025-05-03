from typing import Literal

from pydantic import BaseModel, Field, ConfigDict, EmailStr


class TokenSchema(BaseModel):
    access_token: str | None
    refresh_token: str | None
    token_type: Literal["Bearer"] = "Bearer"


class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(examples=["password"])


class AccessTokenPayloadSchema(BaseModel):
    user_id: int


class RefreshTokenPayloadSchema(BaseModel):
    user_id: int
    jti: str
    fingerprint: str

    model_config = ConfigDict(from_attributes=True)


class BaseRegisterSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    email: EmailStr
    password: str = Field(min_length=8)
    password_repeat: str = Field(min_length=8)


class RegisterUniversitySchema(BaseRegisterSchema):
    name: str


class RegisterTeacherSchema(BaseRegisterSchema):
    departments_id: int
    institute_id: int


class RegisterStudentSchema(BaseRegisterSchema):
    group_id: int
    grade_book_number: str
    student_card: str
