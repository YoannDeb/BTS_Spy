# Better to have Phyton > 3.2.2 for decent html.parser

import requests
from bs4 import BeautifulSoup

product_page_url = "http://books.toscrape.com/catalogue/dune-dune-1_151/index.html"

page_content = requests.get(product_page_url)


page_soup = BeautifulSoup(page_content.text, "html.parser")



title = page_soup.select('h1')[0].text # Select Title, extract from list and isolate text
table = page_soup.select('table.table-striped tr td')
universal_product_code = table[0].text
price_including_tax = table[3].text
price_excluding_tax = table[2].text
number_available = table[5].text

product_description = page_soup.select("#product_description ~ p")[0].text # selects the next sibling after the div with id=product-description

category = page_soup.select('.breadcrumb > li:nth-of-type(3) > a')[0].text


print("product_page_url : ", product_page_url)
print("Universal_product-code (upc) : ", universal_product_code)
print("title : ", title)
print("price_including_tax", price_including_tax)
print("price_excluding_tax", price_excluding_tax)
print("number_available", number_available)
print("product_description : ", product_description)
print("category :", category)