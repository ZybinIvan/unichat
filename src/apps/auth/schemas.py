from typing import Literal

from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str | None
    refresh_token: str | None
    token_type: Literal["Bearer"] = "Bearer"


class LoginSchema(BaseModel):
    phone: str = Field(examples=["79999999999"])
    password: str = Field(examples=["password"])