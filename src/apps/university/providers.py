# src/apps/university/depends.py
from dishka import Provider, Scope, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from src.apps.university.department.repositories import DepartmentRepository
from src.apps.university.department.services import DepartmentService
from src.apps.university.department.use_cases import CreateDepartmentUseCase, RetrieveDepartmentUseCase, \
    ListDepartmentsUseCase, UpdateDepartmentUseCase, DeleteDepartmentUseCase
from src.apps.university.group.repositories import GroupRepository
from src.apps.university.group.services import GroupService
from src.apps.university.group.use_cases import CreateGroupUseCase, RetrieveGroupUseCase, ListGroupsUseCase, \
    UpdateGroupUseCase, DeleteGroupUseCase
from src.apps.university.institute.repositories import InstituteRepository
from src.apps.university.institute.services import InstituteService
from src.apps.university.institute.use_cases import CreateInstituteUseCase, RetrieveInstituteUseCase, \
    ListInstitutesUseCase, UpdateInstituteUseCase, DeleteInstituteUseCase
from src.apps.university.repositories import (
    UniversityRepository,
)
from src.apps.university.services import (
    UniversityService,
)
from src.apps.user.repositories import UniversityAdminRepository

# 1. Провайдер для всех компонентов вашего модуля University
university_provider = Provider(scope=Scope.REQUEST)

# — регистрация репозиториев —
university_provider.provide(UniversityRepository)
university_provider.provide(UniversityAdminRepository)
university_provider.provide(InstituteRepository)
university_provider.provide(DepartmentRepository)
university_provider.provide(GroupRepository)

# — регистрация сервисов (зависимость от репозиториев разрешится автоматически) —
university_provider.provide(UniversityService)

# — регистрация use-case’ов (зависимость от сервисов) —
university_provider.provide(CreateInstituteUseCase)
university_provider.provide(CreateDepartmentUseCase)
university_provider.provide(CreateGroupUseCase)

university_provider.provide(InstituteService)
university_provider.provide(RetrieveInstituteUseCase)
university_provider.provide(ListInstitutesUseCase)
university_provider.provide(UpdateInstituteUseCase)
university_provider.provide(DeleteInstituteUseCase)

university_provider.provide(DepartmentService)
university_provider.provide(RetrieveDepartmentUseCase)
university_provider.provide(ListDepartmentsUseCase)
university_provider.provide(UpdateDepartmentUseCase)
university_provider.provide(DeleteDepartmentUseCase)

university_provider.provide(GroupService)
university_provider.provide(RetrieveGroupUseCase)
university_provider.provide(ListGroupsUseCase)
university_provider.provide(UpdateGroupUseCase)
university_provider.provide(DeleteGroupUseCase)
university_provider.provide(UniversityRepository)



