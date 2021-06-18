# Better to have Python > 3.2.2 for decent html.parser (if using html.parser)

import requests
from bs4 import BeautifulSoup

# define BookToScrape URL
bts_url = "http://books.toscrape.com"
bts_url_catalogue = bts_url + "/catalogue"
# defining page URL
cat_name = "travel_2"
cat_url = "http://books.toscrape.com/catalogue/category/books/" + cat_name + "/index.html"
# Todo mise en page selon la norme PEP8
# Todo change reviews in numbers
# Todo download images


# extracting page from url, testing connexion and make soup
def extract_soup(url):
    while True:
        page_content = requests.get(url)
        if page_content.ok:
            break
        else:
            print("HTTP Error : ", page_content)
            user_choice = input("Press Enter to retry, Q to quit program: ")
            if user_choice.capitalize() == "Q":
                exit()
    page_soup = BeautifulSoup(page_content.content, "html.parser")
    return page_soup


# Calculates a superior round
def ceil(number):
    if number % 1 == 0 :
        number=int(number)
    else:
        number = int(number) + 1
    return number


# Calculates the number of pages in a category
# and generates a list of pages
def list_of_pages_in_category(cat_url, cat_name):
    book_number = extract_soup(cat_url).select_one('.form-horizontal > strong').text
    nb_pages = ceil(int(book_number) / 20)
    cat_urls_list = [cat_url]
    for nb_page in range(2, nb_pages+1):
        cat_urls_list.append(bts_url_catalogue + "/category/books/" + cat_name + "/page-" + str(nb_page) + ".html"  )
    return cat_urls_list


# find all book links in a category
def book_links(cat_urls_list):
    raw_links = []
    for page in range(0, len(cat_urls_list)):
        page_soup = extract_soup(cat_urls_list[page])
        raw_links = raw_links + page_soup.select('h3 > a')
    clean_links = []
    for raw_link in raw_links:
        clean_links.append(bts_url_catalogue + raw_link['href'][8:])
    return clean_links


# Extracting info in book page
def extract_info(product_page_url, bts_url):
    page_soup = extract_soup(product_page_url)
    # Selecting Title, extract from list and isolate text and format with quotes
    title = '"' + page_soup.select_one('h1').text.replace('"', '') + '"'
    # Selecting "Product Information" Table td content and store it in a list
    table = page_soup.select('table.table-striped tr td')
    # Extracting wanted informations from table list
    universal_product_code = table[0].text
    price_including_tax = table[3].text# Strangely the first character is a bug probably from some encoding mystery
    price_excluding_tax = table[2].text
    number_available = table[5].text.replace("In stock (", "").replace(" available)", "")
    print(price_including_tax)
    print(price_excluding_tax)
    # Selecting product_description
    # selects the next sibling after the div with id=product-description
    product_description = page_soup.select_one("#product_description ~ p")
    print(product_description)
    # Checks if product description exists ; if no, replace with something, if yes format for CSV
    if product_description is None:
        product_description ='"Non renseigné"'
    else:
        product_description = '"' + product_description.text.replace('"', '').replace(' ...more', '') + '"'
    # Selecting category
    category = page_soup.select_one('.breadcrumb > li:nth-of-type(3) > a').text

    # Extracting review_rating
    review_rating = page_soup.select_one('.star-rating').get('class')[1]  # todo Poser la question : Pourquoi .p ne marche pas ?

    # Extracting img relative url "src=", truncate and concatenate with bts_url to form complete URL
    image_url = bts_url + page_soup.select_one("#product_gallery .item").img['src'][5:]
    # Making list for one book
    list_info = (product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url)
    return list_info

def init_csv(cat_name):
    with open(cat_name + '.csv', 'w') as cat_name:
        print("product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url", file=cat_name)

def append_csv(cat_name, list_info):
    with open(cat_name + '.csv', 'a') as cat_name:
        print(list_info[0] + "," + list_info[1] + "," + list_info[2]
              + "," + list_info[3] + "," + list_info[4] + ","
              + list_info[5] + "," + list_info[6]
              + "," + list_info[7] + "," + list_info[8] + ","
              + list_info[9], file=cat_name)


links = book_links(list_of_pages_in_category(cat_url, cat_name))
init_csv(cat_name)
for link in links:
    append_csv(cat_name, extract_info(link, bts_url))

# CSV Generation todo save in a folder

