from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_session

SessionDepends = Annotated[AsyncSession, Depends(get_session)]