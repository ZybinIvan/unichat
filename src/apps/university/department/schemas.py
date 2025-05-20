from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, ConfigDict

from src.apps.university.institute.schemas import InstituteResponseSchema
from src.apps.university.models import DepartmentModel


class DepartmentCreateSchema(BaseModel):
    institute_id: int
    name: str


class DepartmentResponseSchema(BaseModel):
    id: int
    institute_id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class DepartmentListResponseSchema(BaseModel):
    total_count: int
    data: list[DepartmentResponseSchema]

    model_config = ConfigDict(from_attributes=True)


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
