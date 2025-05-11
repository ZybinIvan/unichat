# src/apps/university/depends.py
from dishka import Provider, Scope, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from src.apps.university.repositories import (
    UniversityRepository,
    InstituteRepository,
    DepartmentRepository,
    GroupRepository,
)
from src.apps.university.services import (
    UniversityService,
    InstituteService,
    DepartmentService,
    GroupService,
)
from src.apps.university.use_cases import (
    CreateInstituteUseCase,
    CreateDepartmentUseCase,
    CreateGroupUseCase,
    DeleteDepartmentUseCase,
    DeleteGroupUseCase,
    DeleteInstituteUseCase,
    ListDepartmentsUseCase,
    ListGroupsUseCase,
    ListInstitutesUseCase,
    RetrieveDepartmentUseCase,
    RetrieveGroupUseCase,
    RetrieveInstituteUseCase,
    UpdateDepartmentUseCase,
    UpdateGroupUseCase,
    UpdateInstituteUseCase,
)

# 1. Провайдер для всех компонентов вашего модуля University
university_provider = Provider(scope=Scope.REQUEST)

# — регистрация репозиториев —
university_provider.provide(UniversityRepository)
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

# 2. Собираем контейнер, добавляя FastapiProvider для работы с Request
container = make_async_container(
    university_provider,
    FastapiProvider(),
)

# 3. Экспортируем контейнер и используемые в роутере типы
#    (далее в main.py подключите setup_dishka(container, app))
__all__ = [
    "container",
]
