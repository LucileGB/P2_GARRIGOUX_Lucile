import argparse
import time

from scraping import Scraper


def set_delay():
    delay = 0
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--delay",
        help="Intervalle entre chaque scrape de livre (unité de base : seconde).",
        type=float,
    )
    args = parser.parse_args()

    if args.delay:
        if args.delay > 0:
            delay = float(args.delay)

    return delay


if __name__ == "__main__":
    """Allow the user to set the delay between two book scrapes if wished."""
    delay = set_delay()
    start = int(time.time())

    print(f"Scraping commencé à {time.strftime('%T')}...")

    scraper = Scraper(delay)
    scraper.init_scraping()

    end = time.time()
    duration = int(end - start)

    print(f"Scraping terminé à {time.strftime('%T')}.")
    print(f"Durée : {duration} secondes, soit {round(duration/60)} minutes.")
