from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base


class Talk(Base):
    __tablename__ = "talks"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int]

    # Sentence : Talk = 1 : 1
    sentence_id: Mapped[int] = ForeignKey("sentences.id")
    sentence: Mapped["Sentence"] = relationship("Sentence", uselist=False)

    # History : Talk = 1 : n
    history_id: Mapped[int] = mapped_column(ForeignKey("histories.id"))

    def __repr__(self) -> str:
        return (
            "<Talk (id, order, sentence)"
            + f" = ({self.id}, {self.order_id}, {self.sentence.sentence})>"
        )
