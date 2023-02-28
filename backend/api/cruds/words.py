from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.models.sentences import Sentence as SentenceModel
from api.models.words import Word as WordModel
from api.schemas import sentences as sentence_schema
from api.schemas import words as word_schema


async def get_all_words(db: AsyncSession) -> List[WordModel]:
    results = await db.execute(select(WordModel))
    return results.scalars().all()


async def find_by_id(db: AsyncSession, word_id: int) -> WordModel | None:
    result = await db.execute(select(WordModel).where(WordModel.id == word_id))
    return result.scalar()


async def create_word(db: AsyncSession, word_body: word_schema.WordCreate) -> WordModel:
    word = WordModel(**word_body.dict())

    db.add(word)
    await db.commit()
    await db.refresh(word)

    return word
