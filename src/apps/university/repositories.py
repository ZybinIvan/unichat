from src.core.repositories import BaseRepository
from .models import UniversityModel


class UniversityRepository(BaseRepository[UniversityModel]):
    model = UniversityModel
