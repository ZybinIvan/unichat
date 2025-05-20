import logging

from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from src.apps.university.models import InstituteModel
from src.core.exceptions import OperationFailedException
from src.core.repositories import BaseRepository

logger = logging.getLogger(__name__)

class InstituteRepository(BaseRepository[InstituteModel]):
    model = InstituteModel

