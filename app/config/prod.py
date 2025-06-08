from pydantic_settings import BaseSettings


class ProdSettings(BaseSettings):
    # Bot token
    BOT_TOKEN: str

    # MongoDB
    MONGODB_NAME: str
    MONGODB_URL: str
    MONGODB_USER: str
    MONGODB_PASSWORD: str
    MONGODB_HOST: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
