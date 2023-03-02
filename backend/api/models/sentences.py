from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base


class Sentence(Base):
    __tablename__ = "sentences"

    id: Mapped[int] = mapped_column(primary_key=True)
    sentence: Mapped[str]
    translation: Mapped[str]
    counter: Mapped[int] = mapped_column(default=0)

    # Sentence : Talk = 1 : 1
    # Talk - some sentences has no relation to talk
    talk: Mapped["Talk"] = relationship(uselist=False, back_populates="sentence")

    def __repr__(self) -> str:
        return (
            "<Sentence (id, sent, trans, counter, talk)"
            + f" = ({self.id}, {self.sentence}, {self.translation}, {self.counter}, {self.talk})>"
        )
