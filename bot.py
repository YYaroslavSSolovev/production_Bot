import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from config import BOT_TOKEN, REDIS_URL, ADMIN_ID
from database.db import init_db
from handlers import user, admin
from services.scheduler import start_scheduler, add_user_timezone_job


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


logger = logging.getLogger(__name__)


async def main():
    setup_logging()
    logger.info("Starting bot...")

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    redis = Redis.from_url(REDIS_URL)
    storage = RedisStorage(redis=redis)
    dp = Dispatcher(storage=storage)

    await init_db()

    dp.include_router(user.router)
    dp.include_router(admin.router)

    start_scheduler()
    add_user_timezone_job(bot, ADMIN_ID, "Europe/Moscow")

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot started")

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        await redis.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")