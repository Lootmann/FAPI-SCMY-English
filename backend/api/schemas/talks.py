from pydantic import BaseModel, Field, validator

from api.schemas import sentences as sentence_schema


class TalkBase(BaseModel):
    class Config:
        orm_mode = True


class TalkCreate(TalkBase):
    sentence: sentence_schema.SentenceCreate


class TalkCreateResponse(TalkBase):
    id: int
    order_id: int
    sentence: sentence_schema.SentenceCreateResponse


class Talk(TalkBase):
    id: int
    order_id: int
    sentence: sentence_schema.Sentence
