from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, HTMLResponse
from fastapi.exceptions import HTTPException
import os
import threading
import time
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from src import feeder
import requests
import random


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    # "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "it-IT,it;q=0.9",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
}


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
    endpoints = [
        "morning", "globo", "tienimi-bordone",
        "ascolta", "amare-parole", "ci-vuole-una-scienza",
        "altre-indagini", "podcast-eurovision", "wilson"
    ]
    random.shuffle(endpoints)
    with requests.Session() as session:
        session.headers = headers
        for endpoint in endpoints:
            url = "https://www.ilpost.it/podcasts/" + endpoint
            feeder.podgen(url, f"ilpost/{endpoint}.xml", session)

def scheduled_task() -> None:
    """A sample scheduled task executed every day at 8:25 AM."""
    update_podcasts()
    while True:
        now = datetime.now()
        next_run = now.replace(hour=8 - 1, minute=25, second=0, microsecond=0)
        if now > next_run:
            next_run += timedelta(days=1)
        sleep_time = (next_run - now).total_seconds()
        time.sleep(sleep_time)
        update_podcasts()

@app.get("/")
async def home() -> HTMLResponse:
    filepath = "ilpost/home.html"
    with open(filepath, "r") as f:
        data = f.read()
    return HTMLResponse(content=data)

@app.get("/ilpost/{filename}")
async def get_feed(filename: str) -> PlainTextResponse:
    """Return the content of a file from the 'ilpost' directory."""
    filepath = os.path.join("ilpost", filename)
    if not os.path.isfile(filepath) or not filepath.endswith(".xml"):
        raise HTTPException(status_code=404, detail="File not found")
    with open(filepath, "r") as f:
        data = f.read()
    return PlainTextResponse(data)


