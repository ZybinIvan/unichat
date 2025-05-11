from src.core.repositories import BaseRepository
from .models import UniversityModel, DepartmentModel, GroupModel, InstituteModel


class UniversityRepository(BaseRepository[UniversityModel]):
    model = UniversityModel


class InstituteRepository(BaseRepository[InstituteModel]):
    model = InstituteModel


class DepartmentRepository(BaseRepository[DepartmentModel]):
    model = DepartmentModel


class GroupRepository(BaseRepository[GroupModel]):
    model = GroupModel
