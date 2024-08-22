"""Server app config."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from beanie import Document, init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from config import CONFIG
from storage.db.connection import init_connection
import logging
from starlette.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)

DATABASE_URI = CONFIG.mongo_uri
DATABASE_NAME = CONFIG.mongo_name


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_connection(DATABASE_URI, DATABASE_NAME)
        print("Startup completed!")
        yield
        print("Shutdown completed!")
    except:
        logger.error("Database connection error")
        raise HTTPException(status_code=500, detail="Database connection error")

app = FastAPI(
    title="Forehouse Backend",
    description="Backend for Forehouse project",
    version="0.1.0",
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
