from typing import List

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.models.histories import History as HistoryModel
from api.models.sentences import Sentence as SentenceModel
from api.models.talks import Talk as TalkModel
from api.schemas import talks as talk_schema


def get_all_talks(db: AsyncSession) -> List[TalkModel]:
    return db.query(TalkModel).all()


def create_talk(
    db: AsyncSession, sentence: SentenceModel, history: HistoryModel
) -> TalkModel:
    """
    create sentence
    attach to talk
    append talk to history
    """
    print("\n>>> cruds create_talk")

    # create new sentence
    # IMPL: get latest history's talk order_id
    print("1")
    order_id = 0

    for talk in history.talks:
        order_id = max(order_id, talk.id)

    # IMPL: Create new talk, and generate relations between talk and sentence
    print("2")
    talk = TalkModel(order_id=order_id + 1, sentence=sentence)
    db.add(sentence)
    db.refresh(sentence)
    db.commit()

    db.add(talk)
    db.refresh(talk)
    db.commit()

    history.talks.append(talk)

    db.add(history)
    db.commit()
    db.refresh(history)

    # IMPL: return new adding talk
    print("3")
    return talk
