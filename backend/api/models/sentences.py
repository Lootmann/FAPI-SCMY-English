from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base


class Sentence(Base):
    __tablename__ = "sentences"

    id: Mapped[int] = mapped_column(primary_key=True)
    sentence: Mapped[str]
    translation: Mapped[str]
    counter: Mapped[int]

    def __repr__(self) -> str:
        return f"<Sentence (id, sent, trans, conter) = ({self.id}, {self.sentence}, {self.translation}, {self.counter})>"
