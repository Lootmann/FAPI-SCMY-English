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


async def update_sentence(
    db: AsyncSession,
    original: SentenceModel,
    sentence_body: sentence_schema.SentenceUpdate,
) -> SentenceModel:
    if sentence_body.sentence != "":
        original.sentence = sentence_body.sentence

    if sentence_body.translation != "":
        original.translation = sentence_body.translation

    db.add(original)
    await db.commit()
    await db.refresh(original)

    return original


async def delete_sentence(db: AsyncSession, sentence: SentenceModel) -> None:
    await db.delete(sentence)
    await db.commit()
    return
