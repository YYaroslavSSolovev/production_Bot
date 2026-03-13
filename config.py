import os
from dotenv import load_dotenv

load_dotenv()


def _require_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise ValueError(f"Environment variable {name} is not set")
    return value


BOT_TOKEN: str = _require_env("BOT_TOKEN")
ADMIN_ID: int = int(_require_env("ADMIN_ID"))
DATABASE_URL: str = _require_env(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@db:5432/demo_bot"
)
REDIS_URL: str = _require_env("REDIS_URL", "redis://redis:6379/0")

COMPANY_INFO: dict = {
    "name": "Demo Company",
    "phone": "+7 (999) 123-45-67",
    "address": "Москва, ул. Примерная, д. 1",
    "hours": "Пн-Пт 9:00-18:00"
}