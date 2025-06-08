import loguru
from config import settings
from db.models import UserStats
from pymongo import AsyncMongoClient


client = AsyncMongoClient(f"{settings.MONGODB_HOST}:27017", username=settings.MONGODB_USER, password=settings.MONGODB_PASSWORD)
db = client["telegram_bot"]
smokers = db["smokers"]


async def save_user_stats(user_stats: UserStats) -> UserStats | None:
    """
    Save user statistics to the MongoDB collection.
    """
    try:
        await smokers.insert_one(user_stats.model_dump())
    except Exception as e:
        loguru.logger.error(f"Error saving user stats: {str(e)}")
        return None

    return user_stats


async def get_user_stats(user_id: str) -> UserStats | None:
    """
    Retrieve user statistics from the MongoDB collection by user_id.
    """
    try:
        user_stats = await smokers.find_one({"user_id": user_id})
        if user_stats:
            return UserStats(**user_stats)
        else:
            loguru.logger.warning(f"No stats found for user_id: {user_id}")
            return None

    except Exception as e:
        loguru.logger.error(f"Error retrieving user stats: {e}")
        return None


async def update_stats() -> None:
    """
    Update user statistics in the MongoDB collection by user_id.
    """
    try:
        result = await smokers.update_many(
            {},
            {"$inc": {"counter": 1, "saved_money": 20}}
        )
        if result is None:
            loguru.logger.warning(f"Update operation returned None")
            return None

    except Exception as e:
        loguru.logger.error(f"Error updating user stats: {e}")
        return None


async def get_all_user_stats() -> list[UserStats]:
    """
    Retrieve all user statistics from the MongoDB collection.
    """
    try:
        users = await smokers.find().to_list(length=None)
        return [UserStats(**user) for user in users]

    except Exception as e:
        loguru.logger.error(f"Error retrieving all user stats: {e}")
        return []
