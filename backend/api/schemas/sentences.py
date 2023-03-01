from pydantic import BaseModel, Field, validator


class SentenceBase(BaseModel):
    sentence: str = Field("")
    translation: str = Field("")

    class Config:
        orm_mode = True


class SentenceCreate(SentenceBase):
    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "sentence": "Example",
                "translation": "さんぷる",
            }
        }


class SentenceCreateResponse(SentenceCreate):
    id: int
    counter: int


class SentenceUpdate(BaseModel):
    sentence: str = Field("")
    translation: str = Field("")

    class Config:
        schema_extra = {
            "example": {
                "sentence": "Example",
                "translation": "さんぷる",
            }
        }


class Sentence(SentenceBase):
    id: int
