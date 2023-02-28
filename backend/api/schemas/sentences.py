from pydantic import BaseModel, Field, validator


class SentenceBase(BaseModel):
    sentence: str = Field("")
    translation: str = Field("")

    class Config:
        orm_mode = True

        extra_schema = {
            "example": {
                "sentence": "Example",
                "translation": "さんぷる",
            }
        }


class SentenceCreate(SentenceBase):
    pass


class SentenceCreateResponse(SentenceCreate):
    id: int


class Sentence(SentenceBase):
    id: int
