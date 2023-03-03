from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from api.models.sentences import Sentence as SentenceModel
from api.schemas import sentences as sentence_schema


def get_all_sentences(db: Session) -> List[SentenceModel]:
    return db.scalars(select(SentenceModel)).all()


def find_by_id(db: Session, sentence_id: int) -> SentenceModel | None:
    return db.query(SentenceModel).filter(SentenceModel.id == sentence_id).first()


def create_sentence(
    db: Session, sentence_body: sentence_schema.SentenceCreate
) -> SentenceModel:
    sentence = SentenceModel(**sentence_body.dict())

    db.add(sentence)
    db.commit()
    db.refresh(sentence)

    return sentence


def count_sentence(db: Session, sentence: SentenceModel) -> SentenceModel:
    sentence.counter += 1

    db.add(sentence)
    db.commit()
    db.refresh(sentence)

    return sentence


def update_sentence(
    db: Session,
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


def delete_sentence(db: Session, sentence: SentenceModel) -> None:
    db.delete(sentence)
    db.commit()
    return
