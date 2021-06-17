# Better to have Phyton > 3.2.2 for decent html.parser (if using html.parser)

import requests
from bs4 import BeautifulSoup

# define BookToScrape URL
bts_url = "http://books.toscrape.com"
# defining page URL
product_page_url = "http://booksss.toscrape.com/catalogue/dune-dune-1_151/index.html"

# Todo test with html5lib for £ errors

# extracting page from url and testing connexion
while True:
    page_content = requests.get(product_page_url)
    if page_content.ok:
        break
    else:
        print("HTTP Error : ",page_content)
        user_choice = input("Press Enter to retry, Q to quit program: ")
        if user_choice.capitalize()=="Q":
            exit()


# print(page_content.text) # For test purpose

# Parsing page with BeautifulSoup and html.parser
page_soup = BeautifulSoup(page_content.text, "html.parser")
# Selecting Title, extract from list and isolate text
title = page_soup.select_one('h1').text

# Selecting "Product Information" Table td content and store it in a list
table = page_soup.select('table.table-striped tr td')
# Extracting wanted informations from table list
universal_product_code = table[0].text
price_including_tax = table[3].text[1:] # Strangely the first character is a bug probably from some encoding mystery
price_excluding_tax = table[2].text[1:]
number_available = table[5].text.replace("In stock (","").replace(" available)","")

# Selecting product_description
# selects the next sibling after the div with id=product-description
product_description = '"' + page_soup.select_one("#product_description ~ p").text + '"'

# Selecting category
category = page_soup.select_one('.breadcrumb > li:nth-of-type(3) > a').text

# Extracting review_rating
review_rating = page_soup.select_one('.star-rating').get('class')[1] # todo Poser la question : Pourquoi .p ne marche pas ?

# Extracting img relative url "src=", truncate and concatenate with bts_url to form complete URL
image_url = bts_url + page_soup.select_one("#product_gallery .item").img['src'][5:]


# test print
# todo remove test print section
print("product_page_url : ", product_page_url)
print("Universal_product_code : ", universal_product_code)
print("title : ", title)
print("price_including_tax : ", price_including_tax)
print("price_excluding_tax : ", price_excluding_tax)
print("number_available : ", number_available)
print("product_description : ", product_description)
print("category : ", category)
print("review_rating : ", review_rating)
print("image_url : ", image_url)
# end of test print

# CSV Generation todo save in a folder
with open('dune.csv', 'w') as dunecsv:
    print("product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url", file=dunecsv)
    print(product_page_url + "," + universal_product_code + "," + title + "," + price_including_tax + "," + price_excluding_tax + "," + number_available + "," + product_description + "," + category + "," + review_rating + "," + image_url, file=dunecsv)