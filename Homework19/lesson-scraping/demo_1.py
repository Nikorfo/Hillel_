# pip install requests beautifulsoup4 lxml
import requests

HEADERS = { "User-Agent": "hillel-lesson/1.0 (practice)" }

response = requests.get("https://quotes.toscrape.com/", headers=HEADERS, timeout=10)

response.raise_for_status()

# body > div > div:nth-child(2) > div.col-md-8 > div:nth-child(1)
# <p id-"dfdfgse-5665-fg">

# print( response.status_code )
# print( response.headers )
# print( response.encoding )      # iso-8859-1
# print( response.apparent_encoding )

# response.encoding = "utf-8"

# 01101110 01110001 .... 156 77
# ⯢



print( response.text[6:10] )
