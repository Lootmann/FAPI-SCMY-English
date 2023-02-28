from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.cruds import words as word_api
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
    return await word_api.get_all_words(db)


@router.get(
    "/words/{word_id}",
    response_model=word_schema.Word,
    status_code=status.HTTP_200_OK,
)
async def get_word(
    word_id: int,
    db: AsyncSession = Depends(get_db),
):
    word = await word_api.find_by_id(db, word_id)
    if not word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Word: {word_id} Not Found"
        )
    return word


@router.post(
    "/words",
    response_model=word_schema.WordCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_word(
    word_body: word_schema.WordCreate,
    db: AsyncSession = Depends(get_db),
):
    # TODO: validation - dup word is not allowed.
    return await word_api.create_word(db, word_body)
