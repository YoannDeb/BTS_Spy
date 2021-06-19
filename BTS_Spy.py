# Better to have Python > 3.2.2 for decent html.parser (if using html.parser)

import pathlib
import os
import requests
from bs4 import BeautifulSoup

# define BookToScrape URL
BTS_URL = "http://books.toscrape.com"
# Todo mise en page selon la norme PEP8 et PEP20
# Todo download images # Todo slugify title to use like an image name # Todo rajouter dans le csv le chemin et nom de l'image ?
# Todo improve url and csv filenames with f" exemple f"{BTS_URL}/catalogue/{raw_link[‘href’][8:]}" + replace constant BTS_URL by the text in the document ?
# Todo réduction et mise en page des commentaires (notamment juste après le def pour décrire un fonction) net suppression des commentaires en trop
# Todo commit plus clairs et normalisés
# Todo mettre __author__
# Todo mettre fonction __main__ et fonction principale (entry_point() ou BTS_Spy_job())
# todo mettre en forme readme.md avec mise en forme Markdown et deux fichier anglais et fr
# todo .gitignore
# todo import math et use ceil
# todo librairie pour faire un csv à partir d'une liste ?
# todo faire une presentation


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
        clean_links.append(BTS_URL + "/catalogue" + raw_link['href'][8:])
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
        product_description = '"Non renseigné"'
    else:
        product_description = '"' + product_description.text.replace('"', '').replace(' ...more', '') + '"'
    # Extracting category
    category = '"' + page_soup.select_one('.breadcrumb > li:nth-of-type(3) > a').text + '"'
    # Extracting review_rating
    review_rating = page_soup.select_one('.star-rating').get('class')[1].replace("One", "1").replace("Two", "2").replace("Three", "3").replace("Four", "4").replace("Five", "5")
    # Extracting img relative url "src=", truncate and concatenate with BTS_URL to form complete URL
    image_url = BTS_URL + page_soup.select_one("#product_gallery .item").img['src'][5:]
    # getting image relative path
#    get_image_path_from_url(product_page_irl)
    img_name = product_page_url.replace("http://books.toscrape.com/catalogue/", "").replace("/index.html", "")
    saved_image_path = f"data/{link_cat_name}_img/{img_name}.jpg"
    # Making list for one book
    list_info = (product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url, saved_image_path)
    return list_info


def init_csv():
    with open(pathlib.Path.cwd() / 'data' / csv_name, 'w', encoding='utf-8-sig') as f:
        print("product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url,saved_image_path", file=f)


def append_csv(list_info):
    with open(pathlib.Path.cwd() / 'data' / csv_name, 'a') as f:
        print(list_info[0] + "," + list_info[1] + "," + list_info[2]
              + "," + list_info[3] + "," + list_info[4] + ","
              + list_info[5] + "," + list_info[6]
              + "," + list_info[7] + "," + list_info[8] + ","
              + list_info[9] + "," + list_info[10], file=f)


# todo verbose version. better?
""""
def download_picture(list_info):
    img = requests.get(list_info[-2])
    url_title = list_info[0].replace("http://books.toscrape.com/catalogue/", "").replace("/index.html", "")
    img_name = f"{url_title}.jpg"
    with open(pathlib.Path.cwd() / 'data' / f'{link_cat_name}_img' / img_name, "wb") as i:
        i.write(img.content)
"""
def download_picture(list_info):
    img = requests.get(list_info[-2])
    with open(pathlib.Path.cwd() / 'data' / f'{link_cat_name}_img' / f'{list_info[0].replace("http://books.toscrape.com/catalogue/", "").replace("/index.html", "")}.jpg',"wb") as i:
        i.write(img.content)



# Main Job
# Extracting category url list
cat_urls = extract_cat_urls(BTS_URL)
print("BTS_Spy connected successfully !")
print("The scrapping may take some time...")
print("######################################")

# create data directory if it doesn't exist
os.makedirs(pathlib.Path.cwd() / 'data', exist_ok=True)

csv_counter = 0
book_counter = 0
for cat_url in cat_urls:
    # Defining clean category name
    link_cat_name = cat_url.replace(BTS_URL + "/catalogue/category/books/", "").replace("/index.html", "")

    # Extracting list of book links
    links = book_links(list_of_pages_in_category(cat_url))
    print(f"Processing with {extract_info(links[0])[7]} category")
    print("_________________________________________")
    csv_name = link_cat_name + '.csv'
    os.makedirs(pathlib.Path.cwd() / 'data' / f'{link_cat_name}_img', exist_ok=True)
    init_csv()
    previous_book_counter = book_counter
    for link in links:
        book_info = extract_info(link)
        print(f"{book_counter} book(s) scraped | Processing with book : {book_info[2]}")
        book_counter += 1
        append_csv(book_info)
        download_picture(book_info)
    csv_counter += 1
    print("______________________________________________________________________________________________________")
    print(f"OK ! category n°{csv_counter} with {book_counter - previous_book_counter} book(s) inside completely scraped | {link_cat_name}.csv successfully generated")
    print("______________________________________________________________________________________________________")

print(f"Operation complete, {csv_counter} csv file(s) generated and {book_counter} books scraped. Goodbye !")
