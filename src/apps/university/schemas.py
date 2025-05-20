from pydantic import BaseModel, ConfigDict, EmailStr, Field
from fastapi_filter.contrib.sqlalchemy import Filter

from src.apps.university.models import DepartmentModel, GroupModel, InstituteModel
from src.apps.user.enums import UserRole


class BaseRegisterSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    email: EmailStr
    password: str = Field(min_length=8)
    password_repeat: str = Field(min_length=8)


class RegisterUniversitySchema(BaseRegisterSchema):
    name: str

    model_config = ConfigDict(extra="allow")


class RegisterTeacherSchema(BaseRegisterSchema):
    # department_id: int

    model_config = ConfigDict(extra="allow")


class RegisterStudentSchema(BaseRegisterSchema):
    # group_id: int
    record_book_number: str
    student_card: str
    model_config = ConfigDict(extra="allow")


class UniversityResponseSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserAuthSchema(BaseModel):
    id: int
    university_id: int
    role: UserRole

    model_config = ConfigDict(use_enum_values=True)
