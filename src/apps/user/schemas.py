from pydantic import Field, BaseModel, EmailStr, ConfigDict

from src.apps.user.enums import UserRole


class UserRegisterSchema(BaseModel):
    first_name: str = Field(..., examples=["Константин"])
    last_name: str = Field(..., examples=["Константинов"])
    patronymic: str | None = Field(..., examples=["Константинович"])
    # phone: str
    email: EmailStr
    password: str = Field(min_length=8)
    password_repeat: str = Field(min_length=8)


class UserDetailResponseSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None
    email: str
    role: UserRole

    model_config = ConfigDict(use_enum_values=True, from_attributes=True)


class StudentDetailResponseSchema(UserDetailResponseSchema):
    institute_name: str
    department_name: str
    group_name: str
    record_book_number: str
    student_card: str


class TeacherDetailResponseSchema(UserDetailResponseSchema):
    institute_name: str
    department_name: str


class TeacherResponseSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None


class StudentResponseSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None
