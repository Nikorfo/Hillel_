import requests
from bs4 import BeautifulSoup

import time
import csv


HEADERS = { "User-Agent": "hillel-lesson/1.0 (practice)" }
BASE_URL = "https://quotes.toscrape.com"

def parse_page( url ):
    response = requests.get( url, headers=HEADERS, timeout=10 )
    response.raise_for_status()

    soup = BeautifulSoup( response.text, "lxml" )

    rows = [
        {
            "author": quote.select_one("small.author").get_text(strip=True),
            "text": quote.select_one("span.text").get_text(strip=True).strip("“”"),
            "tags": ", ".join( tag.get_text(strip=True) for tag in quote.select("a.tag") ),
        }
        for quote in soup.select( "div.quote" )           #  div.quote { ... }
    ]

    next_link = soup.select_one("li.next a")
    next_url = BASE_URL + next_link["href"] if next_link else None

    return rows, next_url

def process():
    all_rows = []
    url = BASE_URL + "/"
    page = 1

    while url and page <= 3:
        print(f"Checking page {page}...")
        rows, url = parse_page(url)
        all_rows.extend( rows )
        page += 1
        time.sleep(1)

    return all_rows


def save_data( data ):
    with open("quotes.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["author", "text", "tags"])
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    data = process()

    save_data( data )
