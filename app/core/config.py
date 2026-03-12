from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # PROJECT
    PROJECT_NAME: str = "FASTAPI TEMPLATE"
    VERSION: str = "1.0.0"
    API_STR: str = "/api"
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: list[str] = ["*"]
    # DB
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    # AUTH
    SECRET_KEY: str
    API_KEY: str
    # LOG
    LOG_LEVEL: str = "DEBUG"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    LOG_DIR: str = "logs"
    LOG_FILENAME: str = "file.log"


    @property
    def ASYNC_DATABASE_URI(self) -> str:
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    @property
    def SYNC_DATABASE_URI(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    @property
    def is_dev(self) -> bool:
        return self.ENVIRONMENT == "development"
    

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()