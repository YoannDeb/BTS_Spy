# Better to have Phyton > 3.2.2 for decent html.parser

import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/dune-dune-1_151/index.html"

page_content = requests.get(url)
# print(page_content.status_code)


page_soup = BeautifulSoup(page_content.text, "html.parser")
# print(page_soup)

product_page_url = url
print(url)
title = page_soup.select('h1')
print(title)
table = page_soup.select('table.table-striped tr td')
# table = table.contents
print(table)
product_description = page_soup.find(id="product_description").next_sibling.next_sibling.string
print(product_description)
