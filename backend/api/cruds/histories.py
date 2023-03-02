from typing import List

from sqlalchemy.orm import Session

from api.models.histories import History as HistoryModel


def get_all_histories(db: Session) -> List[HistoryModel]:
    return db.query(HistoryModel).all()


def find_by_id(db: Session, history_id: int) -> HistoryModel:
    return db.query(HistoryModel).filter(HistoryModel.id == history_id).first()


def create_history(db: Session) -> HistoryModel:
    history = HistoryModel()

    db.add(history)
    db.commit()
    db.refresh(history)

    return history


def delete_history(db: Session, history: HistoryModel) -> None:
    db.delete(history)
    db.commit()
    return
