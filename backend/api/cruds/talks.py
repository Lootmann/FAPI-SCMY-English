from typing import List

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from api.models.histories import History as HistoryModel
from api.models.sentences import Sentence as SentenceModel
from api.models.talks import Talk as TalkModel


def get_all_talks(db: Session) -> List[TalkModel]:
    return db.scalars(select(TalkModel)).all()


def create_talk(
    db: Session, sentence: SentenceModel, history: HistoryModel
) -> TalkModel:
    # NOTE: create talk and sentence as same time
    order_id = get_max_talk_order_id(db, history.id)
    talk = TalkModel(order_id=order_id + 1, sentence=sentence)

    db.add(sentence)
    db.add(talk)
    db.commit()

    history.talks.append(talk)

    db.add(history)
    db.commit()

    return talk


def get_all_talks_by_history(db: Session, history_id: int) -> List[TalkModel]:
    return db.scalars(select(TalkModel).where(TalkModel.history_id == history_id)).all()


def get_max_talk_order_id(db: Session, history_id: int) -> int:
    order_id: int | None = db.scalar(
        select(func.max(TalkModel.order_id)).where(TalkModel.history_id == history_id)
    )
    return 0 if not order_id else order_id
