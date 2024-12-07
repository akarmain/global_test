import asyncio
from venv import logger

from sqlalchemy import Column, Integer, String, Boolean, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings import Env

engine = create_async_engine(
    url=str(Env.DATABASE_URL_asyncpg),
    echo=False,
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

Base = declarative_base()


# Описываем модель
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)
    solved = Column(Boolean, default=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with SessionLocal() as session:
        await add_test_data(session)


async def add_test_data(session: AsyncSession):
    result = await session.execute(select(Task))
    existing_data = result.scalars().all()
    if not existing_data:
        test_tasks = [
            Task(id=1, question="1+1", correct_answer="2", solved=False),
            Task(id=2, question="2+3", correct_answer="5", solved=False),
            Task(id=3, question="Hello", correct_answer="world!", solved=False),
        ]
        session.add_all(test_tasks)
        await session.commit()
        logger.info("Тестовые данные успешно добавлены.")
    else:
        logger.info("Тестовые данные уже существуют.")


async def main():
    await init_db()


if __name__ == "__main__":
    asyncio.run(main())
