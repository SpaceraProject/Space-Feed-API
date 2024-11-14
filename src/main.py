"""
Main module for the RESTAPI
"""
import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from utils import check_rss, last_articles
from models import Article

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()
INTERVAL:int = int(os.getenv("INTERVAL", "10"))
scheduler.add_job(
    check_rss,
    'interval',
    seconds=INTERVAL,
    id='update_articles',
    replace_existing=True
    )

if not scheduler.running:
    logger.info("Starting scheduler")
    scheduler.start()

app = FastAPI(
    title="Space News RESTAPI",
    description="RESTAPI for space news",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root()-> list[Article]:
    """
    Get the last articles
    """
    return last_articles.values()

if __name__ == '__main__':
    uvicorn.run(app)
