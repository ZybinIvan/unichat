from pydantic import BaseModel, EmailStr, Field


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
    department_id: int


class RegisterStudentSchema(BaseRegisterSchema):
    group_id: int
    record_book_number: str
    student_card: str


class UniversityResponseSchema(BaseModel):
    id: int
    name: str


class InstituteCreateSchema(BaseModel):
    university_id: int
    name: str


class InstituteResponseSchema(BaseModel):
    id: int
    name: str
    university_id: int


class DepartmentCreateSchema(BaseModel):
    institute_id: int
    name: str


class DepartmentResponseSchema(BaseModel):
    id: int
    institute_id: int
    name: str


class GroupCreateSchema(BaseModel):
    department_id: int
    name: str


class GroupResponseSchema(BaseModel):
    id: int
    department_id: int
    name: str
