from src.apps.university.models import InstituteModel
from src.core.repositories import BaseRepository


class InstituteRepository(BaseRepository[InstituteModel]):
    model = InstituteModel
