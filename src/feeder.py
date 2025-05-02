from feedgen.feed import FeedGenerator, FeedEntry
from datetime import datetime
from requests import Session
import json
from .fetch import get_data
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_file(filepath: str) -> str:
    with open(filepath, "r") as f:
        return json.loads(f.read())

def generate_rss_feed(podcast: dict) -> FeedGenerator:
    feed = FeedGenerator()
    feed.load_extension("podcast")
    feed.podcast.itunes_category("News", "Podcasting")
    feed.title(podcast["title"])
    feed.link(href=podcast["podcastUrl"], rel="alternate")
    feed.id(podcast["podcastUrl"])
    feed.description(podcast["description"]),
    feed.language("it")
    feed.logo(podcast["image"])
    feed.author({
        "name": podcast["author"],
        "email": podcast["author"].split(" ")[1].lower() + "@ilpost.it"
    })
    return feed

def generate_entry(feed: FeedGenerator, episode: dict) -> FeedEntry:
    entry = feed.add_entry()
    entry.id(episode["episode_raw_url"])
    entry.author({
        "name": episode["author"],
        "email": episode["author"].split(" ")[1].lower() + "@ilpost.it"
    })
    entry.title(episode["title"])
    entry.description(episode["content_html"])
    entry.enclosure(episode["episode_raw_url"], 0, "audio/mpeg")
    entry.published(datetime.fromtimestamp(int(episode["timestamp"])).astimezone())
    return entry

def generate_podcast(data: dict, filepath: str) -> None:
    podcast = data["props"]["pageProps"]["data"]["data"]["podcast"]["data"]
    feed = generate_rss_feed(podcast)
    episodes = data["props"]["pageProps"]["data"]["data"]["episodes"]["data"]
    for episode in episodes:
        generate_entry(feed, episode)
    feed.rss_file(filepath, pretty=True)

def podgen(url: str, filepath: str, session: Session) -> None:
    data = get_data(url, session)
    generate_podcast(data, filepath)
    logging.info(f"Podcast generated! Saved at {filepath}")

def main() -> None:
    podgen(url="https://www.ilpost.it/podcasts/ascolta/", filepath="temp/ascolta.xml")

if __name__ == "__main__":
    main()