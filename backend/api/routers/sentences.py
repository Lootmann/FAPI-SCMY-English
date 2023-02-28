from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.cruds import sentences as sentence_api
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
    return await sentence_api.get_all_sentences(db)


@router.get(
    "/sentences/{sentence_id}",
    response_model=sentence_schema.SentenceCreateResponse,
    status_code=status.HTTP_200_OK,
)
async def get_sentence_by_id(sentence_id: int, db: AsyncSession = Depends(get_db)):
    word = await sentence_api.find_by_id(db, sentence_id)
    if not word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sentence: {sentence_id} Not Found",
        )
    return word


@router.post(
    "/sentences",
    response_model=sentence_schema.SentenceCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_sentence(
    sentence_body: sentence_schema.SentenceCreate,
    db: AsyncSession = Depends(get_db),
):
    # TODO: validaiton - dup sentence isn't allowed
    return await sentence_api.create_sentence(db, sentence_body)
