"""Server main runtime."""

from backend.app import app
from backend.routes.scraped_house import router as scraped_house_router
from backend.routes.data import router as neighborhood_router
from backend.routes.predict_house_price import router as predict_house_price_router

app.include_router(scraped_house_router)
app.include_router(neighborhood_router)

app.include_router(predict_house_price_router)


