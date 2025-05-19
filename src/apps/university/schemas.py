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


class InstituteCreateSchema(BaseModel):
    name: str


class InstituteResponseSchema(BaseModel):
    id: int
    name: str
    university_id: int
    model_config = ConfigDict(from_attributes=True)


class InstituteUpdateSchema(BaseModel):
    name: str | None = None


class InstituteFilter(Filter):
    name__ilike: str | None = None
    university_id: int | None = None
    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = InstituteModel
        ordering_field_name = "order_by"


class DepartmentCreateSchema(BaseModel):
    institute_id: int
    name: str


class DepartmentResponseSchema(BaseModel):
    id: int
    institute_id: int
    name: str


class DepartmentDetailSchema(BaseModel):
    id: int
    name: str
    institute: InstituteResponseSchema

    model_config = ConfigDict(from_attributes=True)


class DepartmentUpdateSchema(BaseModel):
    name: str | None = None
    institute_id: int | None = None


class DepartmentFilter(Filter):
    name__ilike: str | None = None
    institute_id: int | None = None
    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = DepartmentModel
        ordering_field_name = "order_by"


class UserAuthSchema(BaseModel):
    id: int
    university_id: int
    role: UserRole

    model_config = ConfigDict(use_enum_values=True)
