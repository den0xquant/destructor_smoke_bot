from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import settings
from core import messages, serializer
from db.models import UserStats
from db.mongo import get_user_stats, save_user_stats


router = Router()


def get_stats_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📊 Посмотреть статистику", callback_data="stats"
                )
            ]
        ]
    )


@router.message(CommandStart())
async def command_start_handler(message: Message):
    user = message.from_user
    user_stats = UserStats(user_id=str(user.id))
    
    db_user_stats = await get_user_stats(str(user.id))
    if db_user_stats is None:
        await save_user_stats(user_stats)

    await message.answer(messages.START_MESSAGE)


@router.message(Command("stats"))
async def command_stats_handler(message: Message):
    user = message.from_user
    db_user_stats = await get_user_stats(str(user.id))
    if db_user_stats is None:
        await message.answer(messages.NO_STATS_MESSAGE)
        return
    await message.answer(serializer.stats_message(db_user_stats))


def setup_bot() -> Bot:
    return Bot(
        token=settings.BOT_TOKEN,
        default_properties=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


async def main() -> None:
    bot = setup_bot()
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
