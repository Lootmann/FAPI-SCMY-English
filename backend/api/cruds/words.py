from typing import List

from sqlalchemy import func
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


async def find_by_meaning(db: AsyncSession, meaning: str) -> List[WordModel]:
    results = await db.execute(
        select(WordModel).where(WordModel.meaning.icontains(meaning))
    )
    return results.scalars().all()


async def find_by_spell(db: AsyncSession, spell: str) -> List[WordModel]:
    results = await db.execute(
        select(WordModel).where(WordModel.spell.icontains(spell))
    )
    return results.scalars().all()


async def find_by_meaning_and_spell(
    db: AsyncSession, spell: str, meaning: str
) -> List[WordModel]:
    results = await db.execute(
        select(WordModel).where(
            WordModel.spell.icontains(spell) | WordModel.meaning.icontains(meaning)
        )
    )
    return results.scalars().all()


async def exists(db: AsyncSession, spell: str) -> bool:
    result = await db.execute(
        select(WordModel).where(func.lower(WordModel.spell) == func.lower(spell))
    )
    return result.scalar() is not None


async def create_word(db: AsyncSession, word_body: word_schema.WordCreate) -> WordModel:
    word = WordModel(**word_body.dict())

    db.add(word)
    await db.commit()
    await db.refresh(word)

    return word


async def update_word(
    db: AsyncSession, original: WordModel, word_update: word_schema.WordUpdate
) -> WordModel:
    if word_update.spell != "":
        original.spell = word_update.spell

    if word_update.meaning != "":
        original.meaning = word_update.meaning

    db.add(original)
    await db.commit()
    await db.refresh(original)

    return original
