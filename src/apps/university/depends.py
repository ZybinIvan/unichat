from typing import Annotated

from fastapi import Depends

from src.apps.university.repositories import UniversityRepository, DepartmentRepository, GroupRepository, \
    InstituteRepository
from src.apps.university.services import UniversityService, InstituteService, DepartmentService, GroupService
from src.apps.university.use_cases import CreateInstituteUseCase, CreateDepartmentUseCase, CreateGroupUseCase


# ------ РЕПОЗИТОРИИ ------

async def get_university_repository() -> UniversityRepository:
    return UniversityRepository()


UniversityRepositoryDepends = Annotated[UniversityRepository, Depends(get_university_repository)]


async def get_institute_repository() -> InstituteRepository:
    return InstituteRepository()


InstituteRepositoryDepends = Annotated[InstituteRepository, Depends(get_institute_repository)]


async def get_departments_repository() -> DepartmentRepository:
    return DepartmentRepository()


DepartmentRepositoryDepends = Annotated[DepartmentRepository, Depends(get_departments_repository)]


async def get_group_repository() -> GroupRepository:
    return GroupRepository()


GroupRepositoryDepends = Annotated[GroupRepository, Depends(get_group_repository)]


# ------ СЕРВИСЫ ------

async def get_university_service(repository: UniversityRepositoryDepends) -> UniversityService:
    return UniversityService(repository)


UniversityServiceDepends = Annotated[UniversityService, Depends(get_university_service)]


async def get_institute_service(repository: InstituteRepositoryDepends) -> InstituteService:
    return InstituteService(repository)


InstituteServiceDepends = Annotated[InstituteService, Depends(get_institute_service)]


async def get_department_service(repository: DepartmentRepositoryDepends) -> DepartmentService:
    return DepartmentService(repository)


DepartmentServiceDepends = Annotated[DepartmentService, Depends(get_department_service)]


async def get_group_service(repository: GroupRepositoryDepends) -> GroupService:
    return GroupService(repository)


GroupServiceDepends = Annotated[GroupService, Depends(get_group_service)]


# ----- USE CASES ------

async def get_create_institute_use_case(service: InstituteServiceDepends) -> CreateInstituteUseCase:
    return CreateInstituteUseCase(service)


CreateInstituteUseCaseDepends = Annotated[CreateInstituteUseCase, Depends(get_create_institute_use_case)]


async def get_create_department_use_case(service: DepartmentServiceDepends) -> CreateDepartmentUseCase:
    return CreateDepartmentUseCase(service)


CreateDepartmentUseCaseDepends = Annotated[CreateDepartmentUseCase, Depends(get_create_department_use_case)]


async def get_create_group_use_case(service: GroupServiceDepends) -> CreateGroupUseCase:
    return CreateGroupUseCase(service)


CreateGroupUseCaseDepends = Annotated[CreateGroupUseCase, Depends(get_create_group_use_case)]
