from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from api.cruds import histories as history_api
from api.cruds import sentences as sentence_api
from api.cruds import talks as talk_api
from api.db import get_db
from api.schemas import talks as talk_schema

router = APIRouter(tags=["talks"])


@router.get(
    "/talks",
    response_model=List[talk_schema.Talk],
    status_code=status.HTTP_200_OK,
)
def get_all_talks(db: Session = Depends(get_db)):
    return talk_api.get_all_talks(db)


@router.post(
    "/histories/{history_id}/talks",
    response_model=talk_schema.TalkCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_talks(
    history_id: int,
    talk_body: talk_schema.TalkCreate,
    db: Session = Depends(get_db),
):
    print("\n>>> create_talks")

    # create sentence
    sentence = sentence_api.create_sentence(db, talk_body.sentence)

    # get history
    history = history_api.find_by_id(db, history_id)
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"History: {history_id} Not Found",
        )

    print(">>> before")
    talk = talk_api.create_talk(db, sentence, history)
    print(">>> after")
    print(talk)

    return {
        "id": 1,
        "order_id": 1,
        "sentence": {"sentence": "hoge", "translation": "hige", "id": 1, "counter": 0},
    }


@router.get(
    "/histoires/{history_id}/talks",
    response_model=List[talk_schema.Talk],
    status_code=status.HTTP_200_OK,
)
def get_all_talks_by_history_id(history_id: int, db: Session = Depends(get_db)):
    return []
