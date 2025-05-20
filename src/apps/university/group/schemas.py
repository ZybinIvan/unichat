from fastapi_filter import with_prefix, FilterDepends
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Query

from src.apps.university.department.schemas import DepartmentResponseSchema
from src.apps.university.institute.schemas import InstituteResponseSchema, InstituteSimpleSchema
from src.apps.university.models import GroupModel, DepartmentModel, InstituteModel


class GroupCreateSchema(BaseModel):
    department_id: int
    name: str


class GroupResponseSchema(BaseModel):
    id: int
    department: DepartmentResponseSchema
    name: str

    model_config = ConfigDict(from_attributes=True)


class GroupListResponseSchema(BaseModel):
    total_count: int
    data: list[GroupResponseSchema]

    model_config = ConfigDict(from_attributes=True)


class GroupDetailSchema(BaseModel):
    id: int
    name: str
    department: DepartmentResponseSchema

    model_config = ConfigDict(from_attributes=True)


class GroupUpdateSchema(BaseModel):
    name: str | None = None
    department_id: int | None = None


class DepartmentFilter(Filter):
    institute_id: int | None = None

    class Constants(Filter.Constants):
        model = DepartmentModel


class GroupFilter(Filter):
    name__ilike: str | None = None
    department_id: int | None = None
    department: DepartmentFilter = FilterDepends(DepartmentFilter)
    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = GroupModel
        ordering_field_name = "order_by"
