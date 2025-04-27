from pydantic import Field, BaseModel, EmailStr


class UserRegisterSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None
    # phone: str
    email: EmailStr
    password: str = Field(min_length=8)
    password_repeat: str = Field(min_length=8)


class UserResponseSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None
    password: str
    email: str
