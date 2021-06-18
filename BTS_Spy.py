# Better to have Python > 3.2.2 for decent html.parser (if using html.parser)

import pathlib
import os
import requests
from bs4 import BeautifulSoup

# define BookToScrape URL
bts_url = "http://books.toscrape.com"
# Todo mise en page selon la norme PEP8
# Todo download images
# Todo improve url genrating with urllib


# extracting page from url, testing connexion and make soup
def extract_soup(url):
    while True:
        page_content = requests.get(url)
        if page_content.ok:
            break
        else:
            print("HTTP Error: ", page_content, "trying to access: ", url)
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


# Extract categories url list in homepage
def extract_cat_urls(url):
    raw_cat_urls = extract_soup(url).select(".nav-list a")
    # delete "books" false category
    del raw_cat_urls[0]
    clean_cat_urls = []
    for entry in raw_cat_urls:
        clean_cat_urls.append(url + "/" + entry['href'])
    return clean_cat_urls


# Calculates the number of pages in a category and generates a list of pages
def list_of_pages_in_category(cat_url_index):
    # calculates the number of books in one category
    book_number = extract_soup(cat_url_index).select_one('.form-horizontal > strong').text
    nb_pages = ceil(int(book_number) / 20)
    # Initialize all_url_of_one_category with first page of the category
    all_url_of_one_category = [cat_url_index]
    # Iterates pages and appending them to all_url_of_one_category depending on nb_pages
    for nb_page in range(2, nb_pages+1):
        all_url_of_one_category.append(cat_url_index.replace("index", "page-" + str(nb_page)))
    return all_url_of_one_category


# find all book links in a category
def book_links(cat_urls_list):
    raw_links = []
    for page in range(0, len(cat_urls_list)):
        page_soup = extract_soup(cat_urls_list[page])
        raw_links = raw_links + page_soup.select('h3 > a')
    clean_links = []
    for raw_link in raw_links:
        clean_links.append(bts_url + "/catalogue" + raw_link['href'][8:])
    return clean_links


# Extracting info in one book page
def extract_info(product_page_url):
    page_soup = extract_soup(product_page_url)
    # Selecting Title, extract from list and isolate text and format with quotes
    title = '"' + page_soup.select_one('h1').text.replace('"', '') + '"'
    # Selecting "Product Information" Table td content and store it in a list
    table = page_soup.select('table.table-striped tr td')
    # Extracting wanted information from table list
    universal_product_code = table[0].text
    price_including_tax = table[3].text
    price_excluding_tax = table[2].text
    number_available = table[5].text.replace("In stock (", "").replace(" available)", "")
    # Extracting description
    # selects the next sibling after the div with id=product-description
    product_description = page_soup.select_one("#product_description ~ p")
    # Checks if product description exists ; if no, replace with something, if yes format for CSV
    if product_description is None:
        product_description ='"Non renseigné"'
    else:
        product_description = '"' + product_description.text.replace('"', '').replace(' ...more', '') + '"'
    # Extracting category
    category = '"' + page_soup.select_one('.breadcrumb > li:nth-of-type(3) > a').text + '"'
    # Extracting review_rating
    review_rating = page_soup.select_one('.star-rating').get('class')[1].replace("One", "1").replace("Two", "2").replace("Three", "3").replace("Four", "4").replace("Five", "5")
    # Extracting img relative url "src=", truncate and concatenate with bts_url to form complete URL
    image_url = bts_url + page_soup.select_one("#product_gallery .item").img['src'][5:]
    # Making list for one book
    list_info = (product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url)
    return list_info


def init_csv():
    with open(pathlib.Path.cwd() / 'data' / csv_name, 'w', encoding='utf-8-sig') as f:
        print("product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url", file=f)


def append_csv(list_info):
    with open(pathlib.Path.cwd() / 'data' / csv_name, 'a') as f:
        print(list_info[0] + "," + list_info[1] + "," + list_info[2]
              + "," + list_info[3] + "," + list_info[4] + ","
              + list_info[5] + "," + list_info[6]
              + "," + list_info[7] + "," + list_info[8] + ","
              + list_info[9], file=f)

def download_picture(list_info):
    req = requests.get(list_info[-1])
    book_name = list_info[1]
    with open(pathlib.Path.cwd() / 'data' / book_name, "wb") as p:
        for part in req.iter_content:
            p.write(part)



# Extracting category url list
cat_urls = extract_cat_urls(bts_url)

# create data directory if it doesn't exist
os.makedirs(pathlib.Path.cwd() / 'data', exist_ok=True)

csv_number = 0
for cat_url in cat_urls:
    # Defining clean category name
    link_cat_name = cat_url.replace(bts_url + "/catalogue/category/books/", "").replace("/index.html", "")
    print("Processing with " + link_cat_name + " category. Please wait...")
    # Extracting list of book links
    links = book_links(list_of_pages_in_category(cat_url))
    # Extracting info and Exporting into csv TODO save in a folder
    csv_name = link_cat_name + '.csv'
    init_csv()
    for link in links:
        book_info = extract_info(link)
        append_csv(book_info)
        download_picture(book_info)
    csv_number += 1
    print(link_cat_name + ".csv successfully generated")

print("Operation complete, " + str(csv_number) + " file(s) generated. Goodbye !")
