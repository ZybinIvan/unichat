from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, ConfigDict

from src.apps.university.models import InstituteModel
from src.apps.university.schemas import UniversityResponseSchema


class InstituteCreateSchema(BaseModel):
    name: str


class InstituteSimpleSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class InstituteResponseSchema(BaseModel):
    id: int
    name: str
    university: UniversityResponseSchema
    model_config = ConfigDict(from_attributes=True)


class InstituteListResponseSchema(BaseModel):
    total_count: int
    data: list[InstituteResponseSchema]

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
