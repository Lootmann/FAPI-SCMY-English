from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from api.models.sentences import Sentence as SentenceModel
from api.schemas import sentences as sentence_schema


def get_all_sentences(db: AsyncSession) -> List[SentenceModel]:
    results = db.execute(
        select(SentenceModel).options(selectinload(SentenceModel.talk))
    )
    return results.scalars().all()


def find_by_id(db: AsyncSession, sentence_id: int) -> SentenceModel | None:
    result = db.execute(
        select(SentenceModel)
        .where(SentenceModel.id == sentence_id)
        .options(joinedload(SentenceModel.talk))
    )
    return result.scalar()


def create_sentence(
    db: AsyncSession, sentence_body: sentence_schema.SentenceCreate
) -> SentenceModel:
    sentence = SentenceModel(**sentence_body.dict())

    db.add(sentence)
    db.commit()
    db.refresh(sentence)

    return sentence


def count_sentence(db: AsyncSession, sentence: SentenceModel) -> SentenceModel:
    sentence.counter += 1

    db.add(sentence)
    db.commit()
    db.refresh(sentence)

    return sentence


def update_sentence(
    db: AsyncSession,
    original: SentenceModel,
    sentence_body: sentence_schema.SentenceUpdate,
) -> SentenceModel:
    if sentence_body.sentence != "":
        original.sentence = sentence_body.sentence

    if sentence_body.translation != "":
        original.translation = sentence_body.translation

    db.add(original)
    db.commit()
    db.refresh(original)

    return original


def delete_sentence(db: AsyncSession, sentence: SentenceModel) -> None:
    db.delete(sentence)
    db.commit()
    return
