from pydantic_settings import BaseSettings
from pydantic import ConfigDict, computed_field

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    model_config = ConfigDict(
        env_file="../.env",
    )

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
print(settings.DATABASE_URL)  # Теперь используем правильное имя свойства