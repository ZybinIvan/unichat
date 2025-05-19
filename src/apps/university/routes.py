from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from .department.routes import department_router
from .group.routes import group_router
from .institute.routes import institute_router

university_router = APIRouter(route_class=DishkaRoute)

university_router.include_router(institute_router)

university_router.include_router(department_router)

university_router.include_router(group_router)
