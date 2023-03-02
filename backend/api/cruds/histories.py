from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from api.models.histories import History as HistoryModel


async def get_all_histories(db: AsyncSession) -> List[HistoryModel]:
    results = await db.execute(
        select(HistoryModel).options(selectinload(HistoryModel.talks))
    )
    return results.scalars().all()


async def find_by_id(db: AsyncSession, history_id: int) -> HistoryModel:
    result = await db.execute(
        select(HistoryModel)
        .where(HistoryModel.id == history_id)
        .options(selectinload(HistoryModel.talks))
    )
    return result.scalar()


async def create_history(db: AsyncSession) -> HistoryModel:
    history = HistoryModel()

    db.add(history)
    await db.commit()
    await db.refresh(history)

    return history


async def delete_history(db: AsyncSession, history: HistoryModel) -> None:
    await db.delete(history)
    await db.commit()
    return
