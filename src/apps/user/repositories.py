from src.apps.user.models import UserModel, TeacherModel, StudentModel, UniversityAdminModel
from src.core.repositories import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    model = UserModel


class TeacherRepository(BaseRepository[TeacherModel]):
    model = TeacherModel


class StudentRepository(BaseRepository[StudentModel]):
    model = StudentModel


class UniversityAdminRepository(BaseRepository[UniversityAdminModel]):
    model = UniversityAdminModel
