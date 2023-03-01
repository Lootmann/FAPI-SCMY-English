from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base


class Talk(Base):
    __tablename__ = "talks"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int]

    # Sentence
    sentence_id: Mapped[int] = ForeignKey("sentences.id")
    sentence: Mapped["Sentence"] = relationship("Sentence", uselist=False)

    def __repr__(self) -> str:
        return (
            "<Talk (id, order, sentence_id)"
            + f" = ({self.id}, {self.order_id}, {self.sentence_id})>"
        )
