from src.feeder import podgen


def main() -> None:
    urls = [
        "https://www.ilpost.it/podcasts/morning",
        "https://www.ilpost.it/podcasts/globo",
        "https://www.ilpost.it/podcasts/tienimi-bordone",
        "https://www.ilpost.it/podcasts/ascolta",
        "https://www.ilpost.it/podcasts/amare-parole",
        "https://www.ilpost.it/podcasts/ci-vuole-una-scienza",
        "https://www.ilpost.it/podcasts/altre-indagini"
    ]
    for url in urls:
        name = url.split('/')[-1]
        podgen(url, f"ilpost/{name}.xml")

if __name__ == "__main__":
    main()