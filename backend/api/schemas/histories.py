from pydantic import BaseModel


class HistoryBase(BaseModel):
    pass

    class Config:
        orm_mode = True


class HistoryCreate(HistoryBase):
    pass


class HistoryCreateResponse(HistoryCreate):
    id: int


class History(HistoryBase):
    # IMPL: add field 'talks'
    id: int
