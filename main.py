from src import feeder
import requests
import random
import time

def main() -> None:
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
        "https://www.ilpost.it/podcasts/altre-indagini"
    ]
    random.shuffle(urls)
    with requests.Session() as session:
        for url in urls:
            name = url.split('/')[-1]
            feeder.podgen(url, f"ilpost/{name}.xml", session)
            
if __name__ == "__main__":
    main()