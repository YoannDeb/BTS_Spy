# Better to have Python > 3.2.2 for decent html.parser (if using html.parser)

import pathlib
import os

import requests
from bs4 import BeautifulSoup

# Todo mise en page selon la norme PEP8 et PEP20
# Todo download images # Todo slugify title to use like an image name # Todo rajouter dans le csv le chemin et nom de l'image ?
# Todo improve url and csv filenames with f" exemple f"http://books.toscrape.com/catalogue/{raw_link[‘href’][8:]}"
# Todo réduction et mise en page des commentaires (notamment juste après le def pour décrire un fonction) net suppression des commentaires en trop
# Todo commit plus clairs et normalisés
# Todo mettre __author__
# Todo mettre fonction __main__ et fonction principale (entry_point() ou BTS_Spy_job())
# todo mettre en forme readme.md avec mise en forme Markdown et deux fichier anglais et fr
# todo .gitignore
# todo import math et use ceil
# todo librairie pour faire un csv à partir d'une liste ?
# todo faire une presentation


# e
def extract_soup(url):
    """ Extract page from url, test connexion and make soup
    :param url: url of the page to parse
    :return: page parsed
    """

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


def extract_cat_urls(url):
    """ Extract page's category list in homepage.

    :param url: Homepage's url.

    :return: A list of index url of each category.
    """
    raw_cat_urls = extract_soup(url).select(".nav-list a")
    del raw_cat_urls[0]     # delete "books" false category
    clean_cat_urls = []
    for entry in raw_cat_urls:
        clean_cat_urls.append(url + "/" + entry['href'])
    return clean_cat_urls


def list_of_pages_in_category(cat_url_index):
    """ Calculates the number of pages in a category
    and generates the list of pages of this category.

    :param cat_url_index: The index page of the category.

    :return: A list of all pages of the category
    """
    book_number = extract_soup(cat_url_index).select_one('.form-horizontal > strong').text
    nb_pages = ceil(int(book_number) / 20)

    all_url_of_one_category = [cat_url_index]

    for nb_page in range(2, nb_pages+1):
        all_url_of_one_category.append(cat_url_index.replace("index", f"page-{str(nb_page)}"))
    return all_url_of_one_category


def book_links(cat_urls_list):
    """ Find all book's links in one category

    :param cat_urls_list: list of all pages in one category

    :return: a list of all book links in one category
    """
    raw_book_links = []
    for page in range(0, len(cat_urls_list)):
        page_soup = extract_soup(cat_urls_list[page])
        raw_book_links = raw_book_links + page_soup.select('h3 > a')
    clean_book_links = []
    for raw_book_link in raw_book_links:
        clean_book_links.append(f"http://books.toscrape.com/catalogue{raw_book_link['href'][8:]}")
    return clean_book_links


def extract_book_info(product_page_url):
    """ This function extracts all wanted information in one book page

    Those information are :
    - product_page_url
    - universal_product_code
    - title
    - price_including_tax
    - price_excluding_tax
    - number_available
    - product_description
    - category
    - review_rating
    - image_url
    - saved_image_path (/data/category_folder_img whose name
    is created from the name of the category in the url)

    Some variables are surrounded by quotes to comply with csv format

    :param product_page_url: One book's url

    :return: A list of all wanted information for this book
    """

    page_soup = extract_soup(product_page_url)
    title = '"' + page_soup.select_one('h1').text.replace('"', '') + '"'

    # Extracting table which contains the following information
    table = page_soup.select('table.table-striped tr td')

    universal_product_code = table[0].text

    price_including_tax = table[3].text

    price_excluding_tax = table[2].text

    number_available = table[5].text.replace("In stock (", "").replace(" available)", "")

    product_description = page_soup.select_one("#product_description ~ p")
    if product_description is None:
        product_description = '"Non renseigné"'
    else:
        product_description = '"' + product_description.text.replace('"', '').replace(' ...more', '') + '"'

    category = '"' + page_soup.select_one('.breadcrumb > li:nth-of-type(3) > a').text + '"'

    review_rating = page_soup.select_one('.star-rating').get('class')[1].replace("One", "1").replace("Two", "2").replace("Three", "3").replace("Four", "4").replace("Five", "5")

    image_url = "http://books.toscrape.com" + page_soup.select_one("#product_gallery .item").img['src'][5:]

    img_name = product_page_url.replace("http://books.toscrape.com/catalogue", "").replace("/index.html", "")

    saved_image_path = f"data/{link_cat_name}_img/{img_name}.jpg"

    info_list = (product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url, saved_image_path)
    return info_list


def init_csv():
    """ Create the csv file in /data folder.

    The name is from an external variable "csv_name" composed with the name of the book in the url.
    """

    with open(pathlib.Path.cwd() / 'data' / csv_name, 'w', encoding='utf-8-sig') as f:
        print("product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url,saved_image_path", file=f)


def append_csv(info_list):
    """ Print the information in the csv file

    :param info_list: The book information list
    """

    with open(pathlib.Path.cwd() / 'data' / csv_name, 'a') as f:
        print(info_list[0] + "," + info_list[1] + "," + info_list[2]
              + "," + info_list[3] + "," + info_list[4] + ","
              + info_list[5] + "," + info_list[6]
              + "," + info_list[7] + "," + info_list[8] + ","
              + info_list[9] + "," + info_list[10], file=f)


# todo verbose version. better?
""""
def download_picture(info_list):
    img = requests.get(info_list[-2])
    url_title = info_list[0].replace("http://books.toscrape.com/catalogue/", "").replace("/index.html", "")
    img_name = f"{url_title}.jpg"
    with open(pathlib.Path.cwd() / 'data' / f'{link_cat_name}_img' / img_name, "wb") as i:
        i.write(img.content)
"""


def download_picture(info_list):
    """ Downloads the picture of one book from it's information list.

    The name of the .jpeg file is created with the book name in the url

    Save it in a  (
    :param info_list:
    :return:
    """
    img = requests.get(info_list[-2])
    with open(pathlib.Path.cwd() / 'data' / f'{link_cat_name}_img' / f'{info_list[0].replace("http://books.toscrape.com/catalogue/", "").replace("/index.html", "")}.jpg',"wb") as i:
        i.write(img.content)



# Main Job
# Extracting category url list
cat_urls = extract_cat_urls("http://books.toscrape.com")
print("BTS_Spy connected successfully to http://books.toscrape.com !")
print("The scrapping may take some time...")
print("######################################")

os.makedirs(pathlib.Path.cwd() / 'data', exist_ok=True)

csv_counter = 0
book_counter = 0
for cat_url in cat_urls:
    # Defining clean category name
    link_cat_name = cat_url.replace("http://books.toscrape.com/catalogue/category/books/", "").replace("/index.html", "")

    # Extracting list of book links
    links = book_links(list_of_pages_in_category(cat_url))
    print(f"Processing with {extract_book_info(links[0])[7]} category")
    print("_________________________________________")
    csv_name = link_cat_name + '.csv'
    os.makedirs(pathlib.Path.cwd() / 'data' / f'{link_cat_name}_img', exist_ok=True)
    init_csv()
    previous_book_counter = book_counter
    for link in links:
        book_info = extract_book_info(link)
        print(f"{book_counter} book(s) scraped | Processing with book : {book_info[2]}")
        book_counter += 1
        append_csv(book_info)
        download_picture(book_info)
    csv_counter += 1
    print("______________________________________________________________________________________________________")
    print(f"OK ! category n°{csv_counter} with {book_counter - previous_book_counter} book(s) inside completely scraped | {link_cat_name}.csv successfully generated")
    print("______________________________________________________________________________________________________")

print(f"Operation complete, {csv_counter} csv file(s) generated and {book_counter} books scraped. Goodbye !")
