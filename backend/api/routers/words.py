from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_db
from api.schemas import words as word_schema

router = APIRouter(tags=["words"])


@router.get(
    "/words",
    response_model=List[word_schema.Word],
    status_code=status.HTTP_200_OK,
)
async def get_all_words(
    db: AsyncSession = Depends(get_db),
):
    return {"word": "words"}
