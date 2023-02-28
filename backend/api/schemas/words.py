from pydantic import BaseModel, Field, validator


class WordBase(BaseModel):
    spell: str = Field(...)
    meaning: str = Field(...)

    class Config:
        orm_mode = True

        extra_schema = {
            "example": {
                "spell": "hello",
                "meaning": "こんにちは",
            }
        }


class WordCreate(WordBase):
    pass


class WordCreateResponse(WordCreate):
    id: int


class Word(WordBase):
    id: int
