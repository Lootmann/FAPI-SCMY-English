from pydantic import BaseModel, Field, validator


class WordBase(BaseModel):
    spell: str = Field(...)
    meaning: str = Field(...)

    class Config:
        orm_mode = True


class WordCreate(WordBase):
    class Config:
        schema_extra = {
            "example": {
                "spell": "hello",
                "meaning": "こんにちは",
            }
        }


class WordCreateResponse(WordCreate):
    id: int


class WordUpdate(BaseModel):
    spell: str = Field("")
    meaning: str = Field("")

    class Config:
        orm_mode = True


class Word(WordBase):
    id: int
