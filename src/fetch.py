import requests
from bs4 import BeautifulSoup
import json

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

def get_data(url: str) -> dict:
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    raw = soup.find("script", id="__NEXT_DATA__").string
    data = json.loads(raw)
    data["props"]["pageProps"]["data"]["data"]["podcast"]["data"]["podcastUrl"] = url
    return data