import logging
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def send_demo_morning_message(bot: Bot, chat_id: int):
    await bot.send_message(
        chat_id,
        "⏰ Demo scheduled message: good morning! This message was sent by APScheduler."
    )


def add_user_timezone_job(bot: Bot, chat_id: int, user_timezone: str = "Europe/Moscow"):
    scheduler.add_job(
        send_demo_morning_message,
        CronTrigger(hour=8, minute=0, timezone=ZoneInfo(user_timezone)),
        kwargs={"bot": bot, "chat_id": chat_id},
        id=f"morning_{chat_id}",
        replace_existing=True,
    )
    logger.info("Scheduled job created for chat_id=%s tz=%s", chat_id, user_timezone)


def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        logger.info("APScheduler started")