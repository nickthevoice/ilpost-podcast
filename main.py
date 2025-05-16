from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import HTTPException
import os
import threading
import time
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from src import feeder
import requests
import random


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    thread = threading.Thread(target=scheduled_task, daemon=True)
    thread.start()
    yield
    # Shutdown
    # Add any cleanup code here if needed

app = FastAPI(lifespan=lifespan)

def update_podcasts() -> None:
    print("\n--- Welcome to IlPost Podcast ---")
    delay = random.randint(5, 30)
    print(f"Waiting for {delay} seconds")
    time.sleep(delay)
    urls = [
        "https://www.ilpost.it/podcasts/morning",
        "https://www.ilpost.it/podcasts/globo",
        "https://www.ilpost.it/podcasts/tienimi-bordone",
        "https://www.ilpost.it/podcasts/ascolta",
        "https://www.ilpost.it/podcasts/amare-parole",
        "https://www.ilpost.it/podcasts/ci-vuole-una-scienza",
        "https://www.ilpost.it/podcasts/altre-indagini",
        "https://www.ilpost.it/podcasts/podcast-eurovision"
    ]
    random.shuffle(urls)
    with requests.Session() as session:
        for url in urls:
            name = url.split('/')[-1]
            feeder.podgen(url, f"ilpost/{name}.xml", session)

def scheduled_task() -> None:
    """A sample scheduled task executed every day at 8:30 AM."""
    while True:
        now = datetime.now()
        next_run = now.replace(hour=6, minute=25, second=0, microsecond=0)
        if now > next_run:
            next_run += timedelta(days=1)
        sleep_time = (next_run - now).total_seconds()
        time.sleep(sleep_time)
        update_podcasts()

@app.get("/")
async def get_podcast_list() -> list[str]:
    podcasts = os.listdir("ilpost/")
    return [file for file in podcasts if file.endswith(".xml")]

@app.get("/ilpost/{filename}")
async def get_feed(filename: str) -> PlainTextResponse:
    """Return the content of a file from the 'ilpost' directory."""
    filepath = os.path.join("ilpost", filename)
    if not os.path.isfile(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    with open(filepath, "r") as f:
        data = f.read()
    return PlainTextResponse(data)


