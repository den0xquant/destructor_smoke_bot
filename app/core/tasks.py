import asyncio
import logging
import sys

from bot import setup_bot
from core.serializer import reminder_message
from db.mongo import get_all_user_stats
from taskiq import InMemoryBroker, TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', stream=sys.stdout)
logger = logging.getLogger(__name__)

broker = InMemoryBroker()
scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)


@broker.task(schedule=[{"cron": "* * 20 * *"}])
async def send_reminder_message() -> None:
    """Send reminder messages to all users with their current statistics."""
    bot = setup_bot()
    users = await get_all_user_stats()

    for user_stats in users:
        await bot.send_message(
            chat_id=user_stats.user_id,
            text=reminder_message(user_stats),
            disable_notification=True
        )
        await asyncio.sleep(1)
