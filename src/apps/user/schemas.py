from pydantic import Field, BaseModel, EmailStr


class UserRegisterSchema(BaseModel):
    first_name: str = Field(..., examples=["Константин"])
    last_name: str = Field(..., examples=["Константинов"])
    patronymic: str | None = Field(..., examples=["Константинович"])
    # phone: str
    email: EmailStr
    password: str = Field(min_length=8)
    password_repeat: str = Field(min_length=8)


class UserResponseSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None
    email: str


class TeacherResponseSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None


class StudentResponseSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None
