import requests
from bs4 import BeautifulSoup


HEADERS = { "User-Agent": "hillel-lesson/1.0 (practice)" }

response = requests.get("https://quotes.toscrape.com/", headers=HEADERS, timeout=10)

# ------- CHECK

html_data = response.text

soup = BeautifulSoup( html_data, "lxml" )

# site_title = soup.title.text
# print( site_title )

# quote_item = soup.find("div", class_="quote")
# quote_text = quote_item.find("span", class_="text")
# quote_author = quote_item.find("small", class_="author")

# quote_link = quote_item.select_one("a")["href"]

quotes = soup.find_all("div", class_="quote")

print(quotes)
