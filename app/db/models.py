from datetime import datetime

from pydantic import BaseModel, Field


class UserStats(BaseModel):
    user_id: str
    timestamp: datetime = Field(default_factory=datetime.now)

    @property
    def days(self) -> datetime:
        return (datetime.now() - self.timestamp).days
    
    @property
    def saved_money(self) -> int:
        return self.days * 17
