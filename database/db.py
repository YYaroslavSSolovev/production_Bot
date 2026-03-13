from datetime import datetime, timedelta

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import DATABASE_URL
from database.models import Base, Application

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_application(
    user_id: int,
    username: str,
    name: str,
    phone: str,
    description: str
) -> int:
    async with async_session() as session:
        app = Application(
            user_id=user_id,
            username=username,
            name=name,
            phone=phone,
            description=description,
            status="new"
        )
        session.add(app)
        await session.commit()
        await session.refresh(app)
        return app.id


async def get_user_applications(user_id: int) -> list[Application]:
    async with async_session() as session:
        result = await session.execute(
            select(Application)
            .where(Application.user_id == user_id)
            .order_by(Application.created_at.desc())
        )
        return list(result.scalars().all())


async def get_new_applications() -> list[Application]:
    async with async_session() as session:
        result = await session.execute(
            select(Application)
            .where(Application.status == "new")
            .order_by(Application.created_at.desc())
        )
        return list(result.scalars().all())


async def get_all_applications() -> list[Application]:
    async with async_session() as session:
        result = await session.execute(
            select(Application).order_by(Application.created_at.desc())
        )
        return list(result.scalars().all())


async def get_application_by_id(app_id: int) -> Application | None:
    async with async_session() as session:
        result = await session.execute(
            select(Application).where(Application.id == app_id)
        )
        return result.scalar_one_or_none()


async def update_application_status(app_id: int, status: str) -> None:
    async with async_session() as session:
        await session.execute(
            update(Application)
            .where(Application.id == app_id)
            .values(status=status)
        )
        await session.commit()


async def get_statistics() -> dict:
    async with async_session() as session:
        total = await session.scalar(select(func.count()).select_from(Application))
        new = await session.scalar(
            select(func.count()).select_from(Application).where(Application.status == "new")
        )
        accepted = await session.scalar(
            select(func.count()).select_from(Application).where(Application.status == "accepted")
        )
        rejected = await session.scalar(
            select(func.count()).select_from(Application).where(Application.status == "rejected")
        )

        today = datetime.utcnow().date()
        week_ago = today - timedelta(days=7)

        today_count = await session.scalar(
            select(func.count())
            .select_from(Application)
            .where(func.date(Application.created_at) == today)
        )

        week_count = await session.scalar(
            select(func.count())
            .select_from(Application)
            .where(func.date(Application.created_at) >= week_ago)
        )

        return {
            "total": total or 0,
            "new": new or 0,
            "accepted": accepted or 0,
            "rejected": rejected or 0,
            "today": today_count or 0,
            "week": week_count or 0,
        }