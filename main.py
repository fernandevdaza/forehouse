"""Server main runtime."""

from backend.app import app
from backend.routes.scraped_house import router as scraped_house_router
app.include_router(scraped_house_router)

