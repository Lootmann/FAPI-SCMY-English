from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from api.cruds import histories as history_api
from api.db import get_db
from api.schemas import histories as history_schema

router = APIRouter(tags=["histories"])


@router.get(
    "/histories",
    response_model=List[history_schema.History],
    status_code=status.HTTP_200_OK,
)
def get_all_histories(
    db: Session = Depends(get_db),
):
    return history_api.get_all_histories(db)


@router.get(
    "/histories/{history_id}",
    response_model=history_schema.History,
    status_code=status.HTTP_200_OK,
)
def get_history(history_id: int, db: Session = Depends(get_db)):
    history = history_api.find_by_id(db, history_id)
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"History: {history_id} Not Found",
        )
    return history


@router.post(
    "/histories",
    response_model=history_schema.HistoryCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_history(db: Session = Depends(get_db)):
    return history_api.create_history(db)


@router.delete(
    "/histories/{history_id}",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
def delete_history(history_id: int, db: Session = Depends(get_db)):
    history = history_api.find_by_id(db, history_id)
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"History: {history_id} Not Found",
        )
    return history_api.delete_history(db, history)
