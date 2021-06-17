# Better to have Phyton > 3.2.2 for decent html.parser (if using html.parser)

import requests
from bs4 import BeautifulSoup

# define BookToScrape URL
bts_url = "http://books.toscrape.com"
# defining page URL
product_page_url = "http://books.toscrape.com/catalogue/dune-dune-1_151/index.html"

# Todo test of connection, if 200 = ok to go
# Todo test with html5lib for £ errors

# extracting page from url
page_content = requests.get(product_page_url)
# print(page_content.text) # For test purpose

# Parsing page with BeautifulSoup and html.parser
page_soup = BeautifulSoup(page_content.text, "html.parser")
# Selecting Title, extract from list and isolate text
title = page_soup.select_one('h1').text

# Selecting "Product Information" Table td content and store it in a list
table = page_soup.select('table.table-striped tr td')
# Extracting wanted informations from table list
universal_product_code = table[0].text
price_including_tax = table[3].text[1:] # Strangely the first character is a bug probably from encoding
price_excluding_tax = table[2].text[1:]
number_available = table[5].text

# Selecting product_description
# selects the next sibling after the div with id=product-description
product_description = page_soup.select_one("#product_description ~ p").text

# Selecting category
category = page_soup.select_one('.breadcrumb > li:nth-of-type(3) > a').text

# Extracting review_rating
review_rating = page_soup.select_one('.star-rating').get('class')[1] # todo Pourquoi .p ne marche pas ?

# Extracting img relative url "src=", truncate and concatenate with bts_url to form complete URL
image_url = bts_url + page_soup.select_one("#product_gallery .item").img['src'][5:]

# todo créer et remplir fichier csv

# test print
print("product_page_url : ", product_page_url)
print("Universal_product_code : ", universal_product_code)
print("title : ", title)
print("price_including_tax : ", price_including_tax)
print("price_excluding_tax : ", price_excluding_tax)
print("number_available : ", number_available)
print("product_description : ", product_description)
print("category : ", category)
print("review_rating : ", review_rating)
print("image_url : ", image_url) #todo URL en entier ou relative ?
# end of test print