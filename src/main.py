from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from utils import check_rss, last_articles
import logging
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()
INTERVAL:int = int(os.getenv("INTERVAL", 1))
scheduler.add_job(check_rss, 'interval', seconds=INTERVAL+5, id='update_articles', replace_existing=True)
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
async def root():
    return {"message": last_articles}

if __name__ == '__main__':
    uvicorn.run(app)