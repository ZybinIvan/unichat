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

