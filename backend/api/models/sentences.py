from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from api.db import Base


class Sentence(Base):
    __tablename__ = "sentences"

    id: Mapped[int] = mapped_column(primary_key=True)
    sentence: Mapped[str]
    translation: Mapped[str]
    counter: Mapped[int] = mapped_column(default=0)

    # Talk - some sentences has no relation to talk
    talk_id: Mapped[int] = mapped_column(ForeignKey("talks.id"), nullable=True)

    def __repr__(self) -> str:
        return (
            "<Sentence (id, sent, trans, counter, talk)"
            + f" = ({self.id}, {self.sentence}, {self.translation}, {self.counter}, {self.talk_id})>"
        )
