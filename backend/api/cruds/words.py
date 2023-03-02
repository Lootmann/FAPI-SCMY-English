from typing import List

from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from api.models.sentences import Sentence as SentenceModel
from api.models.words import Word as WordModel
from api.schemas import sentences as sentence_schema
from api.schemas import words as word_schema


def get_all_words(db: Session) -> List[WordModel]:
    return db.query(WordModel).all()


def find_by_id(db: Session, word_id: int) -> WordModel | None:
    result = db.execute(select(WordModel).where(WordModel.id == word_id))
    return result.scalar()


def find_by_meaning(db: Session, meaning: str) -> List[WordModel]:
    results = db.execute(select(WordModel).where(WordModel.meaning.icontains(meaning)))
    return results.scalars().all()


def find_by_spell(db: Session, spell: str) -> List[WordModel]:
    results = db.execute(select(WordModel).where(WordModel.spell.icontains(spell)))
    return results.scalars().all()


def find_by_meaning_and_spell(db: Session, spell: str, meaning: str) -> List[WordModel]:
    results = db.execute(
        select(WordModel).where(
            WordModel.spell.icontains(spell) | WordModel.meaning.icontains(meaning)
        )
    )
    return results.scalars().all()


def exists(db: Session, spell: str) -> bool:
    result = db.execute(
        select(WordModel).where(func.lower(WordModel.spell) == func.lower(spell))
    )
    return result.scalar() is not None


def create_word(db: Session, word_body: word_schema.WordCreate) -> WordModel:
    word = WordModel(**word_body.dict())

    db.add(word)
    db.commit()
    db.refresh(word)

    return word


def update_word(
    db: Session, original: WordModel, word_update: word_schema.WordUpdate
) -> WordModel:
    if word_update.spell != "":
        original.spell = word_update.spell

    if word_update.meaning != "":
        original.meaning = word_update.meaning

    db.add(original)
    db.commit()
    db.refresh(original)

    return original


def delete_word(db: Session, original: WordModel) -> None:
    db.delete(original)
    db.commit()
    return
