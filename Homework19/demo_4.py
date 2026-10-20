import csv

import requests
from bs4 import BeautifulSoup

URL = "https://quotes.toscrape.com/tag/life/"
HEADERS = {"User-Agent": "hillel-lesson/1.0 (practice)"}

response = requests.get(URL, headers=HEADERS, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")

rows = [
    {
        "author": quote.select_one("small.author").get_text(strip=True),
        "text": quote.select_one("span.text").get_text(strip=True).strip("“”"),
    }
    for quote in soup.select("div.quote")
]

with open("life.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["author", "text"])
    writer.writeheader()
    writer.writerows(rows)

print(len(rows))
print(rows[0])   