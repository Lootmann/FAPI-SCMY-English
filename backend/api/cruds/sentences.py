from typing import List

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from api.models.sentences import Sentence as SentenceModel
from api.models.words import Word as WordModel
from api.schemas import sentences as sentence_schema
from api.schemas import words as word_schema


async def get_all_sentences(db: AsyncSession) -> List[SentenceModel]:
    results = await db.execute(select(SentenceModel))
    return results.scalars().all()


async def find_by_id(db: AsyncSession, sentence_id: int) -> SentenceModel | None:
    result = await db.execute(
        select(SentenceModel).where(SentenceModel.id == sentence_id)
    )
    return result.scalar()


async def create_sentence(
    db: AsyncSession, sentence_body: sentence_schema.SentenceCreate
) -> SentenceModel:
    sentence = SentenceModel(**sentence_body.dict())

    db.add(sentence)
    await db.commit()
    await db.refresh(sentence)

    return sentence
