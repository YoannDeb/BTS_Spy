# Better to have Python > 3.2.2 for decent html.parser (if using html.parser)

import requests
from bs4 import BeautifulSoup

# define BookToScrape URL
bts_url = "http://books.toscrape.com"
bts_url_catalogue = bts_url + "/catalogue"
# defining page URL
cat_url = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
cat_name = "Travel"

# Todo test with html5lib for £ errors

# extracting page from url, testing connexion and make soup
def extract_soup(url):
    while True:
        page_content = requests.get(url)
        if page_content.ok:
            break
        else:
            print("HTTP Error : ",page_content)
            user_choice = input("Press Enter to retry, Q to quit program: ")
            if user_choice.capitalize()=="Q":
                exit()
    page_soup = BeautifulSoup(page_content.text, "html.parser")
    return page_soup

# find all book links in a category page # todo page count and explore
def book_links(page_soup):
    links = page_soup.select('h3 > a')
    i = 0
    for link in links: # todo demander si pas plus simple que i
        links[i] = bts_url_catalogue + link.attrs['href'][8:]
        i+=1
    return links

# Extracting info in book page
def extract_info(product_page_url, bts_url):
    page_soup = extract_soup(product_page_url)
    # Selecting Title, extract from list and isolate text
    title = page_soup.select_one('h1').text
    # Selecting "Product Information" Table td content and store it in a list
    table = page_soup.select('table.table-striped tr td')
    # Extracting wanted informations from table list
    universal_product_code = table[0].text
    price_including_tax = table[3].text[1:]  # Strangely the first character is a bug probably from some encoding mystery
    price_excluding_tax = table[2].text[1:]
    number_available = table[5].text.replace("In stock (", "").replace(" available)", "")

    # Selecting product_description
    # selects the next sibling after the div with id=product-description
    product_description = '"' + page_soup.select_one("#product_description ~ p").text + '"'  # todo demander pour les pb de guillemets
    print(product_description) # todo remove after solving encode problem
    # Selecting category
    category = page_soup.select_one('.breadcrumb > li:nth-of-type(3) > a').text

    # Extracting review_rating
    review_rating = page_soup.select_one('.star-rating').get('class')[1]  # todo Poser la question : Pourquoi .p ne marche pas ?

    # Extracting img relative url "src=", truncate and concatenate with bts_url to form complete URL
    image_url = bts_url + page_soup.select_one("#product_gallery .item").img['src'][5:]
    # Making list for one book
    list_info = (product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available,product_description, category, review_rating, image_url)
    return list_info

def init_csv(cat_name):
    with open(cat_name + '.csv', 'w') as cat_name:
        print("product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url", file=cat_name)

def append_csv(cat_name, list_info):
    with open(cat_name + '.csv', 'a') as cat_name:
        print(list_info[0] + "," + list_info[1] + "," + list_info[2] + "," + list_info[3] + "," + list_info[4] + "," + list_info[5] + "," + list_info[6] + "," + list_info[7] + "," + list_info[8] + "," + list_info[9], file=cat_name)

links = book_links(extract_soup(cat_url))
init_csv(cat_name)
for link in links:
    append_csv(cat_name, extract_info(link,bts_url))

exit()


# test print
# todo remove test print section
# print("product_page_url : ", product_page_url)
# print("Universal_product_code : ", universal_product_code)
# print("title : ", title)
# print("price_including_tax : ", price_including_tax)
# print("price_excluding_tax : ", price_excluding_tax)
# print("number_available : ", number_available)
# print("product_description : ", product_description)
# print("category : ", category)
# print("review_rating : ", review_rating)
# print("image_url : ", image_url)
# end of test print

# CSV Generation todo save in a folder

