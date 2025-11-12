import time
import random
import json
from datetime import datetime
from requests import Session
from bs4 import BeautifulSoup


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Sec-Fetch-Site": "same-origin",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Fetch-Mode": "navigate",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Accept-Language": "it-IT,it;q=0.9",
    "Sec-Fetch-Dest": "document",
    "Connection": "keep-alive",
}

def get_data(url: str, session: Session = Session()) -> dict:
    time.sleep(random.randint(1, 3))
    r = session.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    raw = soup.find("script", id="__NEXT_DATA__").string
    data = json.loads(raw)
    data["props"]["pageProps"]["data"]["data"]["podcast"]["data"]["podcastUrl"] = url
    return data

def get_airings_time() -> list[datetime]:
    data = get_data("https://www.ilpost.it/podcasts/morning/")
    episodes = data["props"]["pageProps"]["data"]["data"]["episodes"]["data"]
    return [datetime.fromtimestamp(episode["timestamp"]) for episode in episodes]

def get_next_airing(timings: list[datetime]) -> datetime.time:
    for t in timings:
        print(t)
    return max(t.time() for t in timings)

def main() -> None:
    timings = get_airings_time()
    print(get_next_airing(timings))
 
if __name__ == "__main__":
    main()