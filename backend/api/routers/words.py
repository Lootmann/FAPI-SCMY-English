from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from api.cruds import words as word_api
from api.db import get_db
from api.schemas import words as word_schema

router = APIRouter(tags=["words"])


@router.get(
    "/words",
    response_model=List[word_schema.Word],
    status_code=status.HTTP_200_OK,
)
def get_all_words(db: Session = Depends(get_db)):
    return word_api.get_all_words(db)


@router.get(
    "/words/{word_id}",
    response_model=word_schema.Word,
    status_code=status.HTTP_200_OK,
)
def get_word(
    word_id: int,
    db: Session = Depends(get_db),
):
    word = word_api.find_by_id(db, word_id)
    if not word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Word: {word_id} Not Found"
        )
    return word


@router.get(
    "/words/search/",
    response_model=List[word_schema.Word],
    status_code=status.HTTP_200_OK,
)
def find_by_params(spell: str = "", meaning: str = "", db: Session = Depends(get_db)):
    if spell == "" and meaning == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"No Params",
        )

    if spell == "":
        return word_api.find_by_meaning(db, meaning)
    elif meaning == "":
        return word_api.find_by_spell(db, spell)
    return word_api.find_by_meaning_and_spell(db, spell, meaning)


@router.post(
    "/words",
    response_model=word_schema.WordCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_word(
    word_body: word_schema.WordCreate,
    db: Session = Depends(get_db),
):
    exist_word = word_api.exists(db, word_body.spell)
    if exist_word:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Word: {word_body.spell} already exists",
        )
    return word_api.create_word(db, word_body)


@router.patch(
    "/words/{word_id}",
    response_model=word_schema.WordCreateResponse,
    status_code=status.HTTP_200_OK,
)
def update_word(
    word_id: int,
    word_body: word_schema.WordUpdate,
    db: Session = Depends(get_db),
):
    original_word = word_api.find_by_id(db, word_id)
    if not original_word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Word: {word_id} Not Found",
        )

    if word_body.spell == "" and word_body.meaning == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Word: POST BODY is invalid",
        )

    return word_api.update_word(db, original_word, word_body)


@router.delete("/words/{word_id}", response_model=None, status_code=status.HTTP_200_OK)
def delete(word_id: int, db: Session = Depends(get_db)):
    original = word_api.find_by_id(db, word_id)
    if not original:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Word: {word_id} Not Found",
        )
    return word_api.delete_word(db, original)
