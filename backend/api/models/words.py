from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True)
    spell: Mapped[str]
    meaning: Mapped[str]
    translation: Mapped[str]

    def __repr__(self) -> str:
        return f"<Word (id, spell, mean, trans) = ({self.id}, {self.spell}, {self.meaning}, {self.translation})>"
