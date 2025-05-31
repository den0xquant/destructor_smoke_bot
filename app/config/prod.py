from pydantic_settings import BaseSettings


class ProdSettings(BaseSettings):
    # Bot token
    BOT_TOKEN: str

    # MongoDB
    MONGODB_NAME: str
    MONGODB_URL: str
    MONGO_USER: str
    MONGO_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
