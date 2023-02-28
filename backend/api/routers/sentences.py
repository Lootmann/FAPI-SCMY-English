from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_db
from api.schemas import sentences as sentence_schema

router = APIRouter(tags=["sentences"])


@router.get(
    "/sentences",
    response_model=List[sentence_schema.Sentence],
    status_code=status.HTTP_200_OK,
)
async def get_all_sencentes(
    db: AsyncSession = Depends(get_db),
):
    return {"sentences": "sentences"}
