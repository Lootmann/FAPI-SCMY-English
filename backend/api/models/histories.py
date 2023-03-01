from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base
from api.models.talks import Talk


class History(Base):
    __tablename__ = "histories"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Talk : History = n : 1
    talks: Mapped[List["Talk"]] = relationship("Talk", backref="history")

    def __repr__(self) -> str:
        return f"<History (id, talks) = ({self.id}, {self.talks})>"
