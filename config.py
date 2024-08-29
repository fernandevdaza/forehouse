"""FastAPI server configuration"""

from decouple import config
from pydantic import BaseModel


class Settings(BaseModel):
    """Server config settings."""

    root_url: str = config("ROOT_URL", default="http://localhost:8080")

    mongo_uri: str = config("MONGO_URI")

    mongo_name: str = config("MONGO_DB_NAME")


CONFIG = Settings()
