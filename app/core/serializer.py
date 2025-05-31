from core import messages
from db.models import UserStats


TARGET_DAYS = 90


def plural_days_ru(n: int) -> str:
    if 11 <= n % 100 <= 14:
        suffix = "дней"
    else:
        last_digit = n % 10
        if last_digit == 1:
            suffix = "день"
        elif 2 <= last_digit <= 4:
            suffix = "дня"
        else:
            suffix = "дней"
    return f"{n} {suffix}"


def stats_message(user_stats: UserStats) -> str:
    bar_length = 20
    filled = int((user_stats.days / TARGET_DAYS) * bar_length)
    bar = "🟩" * filled + "⬜" * (bar_length - filled)
    text = messages.STATS_MESSAGE.format(
        days=plural_days_ru(user_stats.days),
        saved_money=user_stats.saved_money,
        target=TARGET_DAYS,
        bar=bar,
    )
    return text


def reminder_message(user_stats: UserStats) -> str:
    text = messages.REMINDER_MESSAGE.format(
        days=plural_days_ru(user_stats.days),
        saved_money=user_stats.saved_money
    )
    return text
