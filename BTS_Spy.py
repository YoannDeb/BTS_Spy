"""
BTS_Spy

Designed to scrape http://books.toscrape.com:
- Create one csv file for each category in data/"name_of_category" folder
- Each csv contains information on each book of the category
- Download the picture of the book in data/"name_of_category"/image folder

(It's better to run on Python > 3.2.2 for decent html.parser)
"""

__author__ = "Yoann Deblois"

import pathlib
import os
import time
import csv
from math import ceil

import requests
from bs4 import BeautifulSoup


def extract_soup(url):
    """
    Parse a page, in other words make soup:
    - Extract page from url
    - Test connexion:
        * if failed propose a retry,
        * else make soup (parse page).

    :param url: Url of the page to parse.
    :return: Soup (page parsed).
    """
    while True:
        page_content = requests.get(url)
        if page_content.ok:
            break
        else:
            print(
                "HTTP Error: ", page_content, "trying to access: ", url)
            user_choice = input(
                "Press Enter to retry, Q to quit program: ")
            if user_choice.capitalize() == "Q":
                exit()
    page_soup = BeautifulSoup(page_content.content, "html.parser")
    return page_soup


def list_cat_index_urls(url):
    """
    List category pages url in homepage.

    :param url: Homepage's url.
    :return: A list of index url of each category.
    """
    raw_cat_urls = extract_soup(url).select(".nav-list a")

    # Delete "books" false category
    del raw_cat_urls[0]
    clean_cat_urls = [f"{url}/{entry['href']}" for entry in raw_cat_urls]
    return clean_cat_urls


def list_pages_in_category(cat_index_url):
    """
    Calculates the number of pages in a category
    and generates the list of pages of this category.

    :param cat_index_url: The index page of the category.
    :return: A list of all pages of the category.
    """
    cat_total_book_number = extract_soup(cat_index_url).select_one(
        '.form-horizontal > strong').text
    nb_pages = ceil(int(cat_total_book_number) / 20)

    # Add index.html first category page to the list
    all_url_of_one_category = [cat_index_url]

    # Append other pages if needed (page-x.html)
    for nb_page in range(2, nb_pages + 1):
        all_url_of_one_category.append(
            cat_index_url.replace("index", f"page-{str(nb_page)}")
        )
    return all_url_of_one_category


def list_book_links(cat_urls_list):
    """
    Find all book's links in one category.

    :param cat_urls_list: List of all pages in one category.
    :return: A list of all book links in one category.
    """
    raw_book_links = []
    for page in cat_urls_list:
        page_soup = extract_soup(page)
        raw_book_links = raw_book_links + page_soup.select('h3 > a')
    clean_book_links = [
        f"http://books.toscrape.com/catalogue{raw_book_link['href'][8:]}"
        for raw_book_link in raw_book_links
    ]
    return clean_book_links


def list_book_info(product_page_url, link_cat_name):
    """
    List all wanted information on a book page.
    Those information are :
    - product_page_url
    - universal_product_code
    - title
    - price_including_tax
    - price_excluding_tax
    - number_available
    - product_description
    - category
    - review_rating (Converted in numbers instead of words)
    - image_url
    - saved_image_path (in folder /data/category_folder_img whose name
    is created from the name of the category in the url,
    and image name created with the book url name shortened to 50 characters)

    Some variables are surrounded by quotes to comply with csv format.

    :param product_page_url: One book's url.
    :param link_cat_name: name of the category as it is in the url.
    :return: A list of all wanted information for this book
    """
    page_soup = extract_soup(product_page_url)
    title = f'"' + page_soup.select_one('h1').text.replace('"', '') + '"'

    # Extracting table which contains several information
    table = page_soup.select('table.table-striped tr td')

    universal_product_code = table[0].text

    price_including_tax = table[3].text

    price_excluding_tax = table[2].text

    number_available = table[5].text.replace(
        "In stock (", "").replace(" available)", "")

    product_description = page_soup.select_one("#product_description ~ p")
    if product_description is None:
        product_description = '"Non renseign??"'
    else:
        product_description = '"' + product_description.text.replace(
            '"', '').replace(' ...more', '') + '"'

    category = '"' + page_soup.select_one(
        '.breadcrumb > li:nth-of-type(3) > a').text + '"'

    review_rating = page_soup.select_one(
        '.star-rating').get('class')[1].replace(
        "One", "1").replace("Two", "2").replace(
        "Three", "3").replace("Four", "4").replace("Five", "5")

    image_url = "http://books.toscrape.com" + page_soup.select_one(
        "#product_gallery .item").img['src'][5:]

    img_name = product_page_url.replace(
        "http://books.toscrape.com/catalogue/", "").replace("/index.html", "")
    saved_image_path = f"data/{link_cat_name}/images/{img_name[:50]}.jpg"

    info_list = [product_page_url, universal_product_code,
                 title, price_including_tax, price_excluding_tax,
                 number_available, product_description, category,
                 review_rating, image_url, saved_image_path]
    return info_list


def create_csv(csv_name, link_cat_name, info_list_of_lists):
    """
    Print the information in the csv file:
    - Write headers
    - For each book write information in one row

    :param csv_name:  Composed with the name of the book in the url.
    :param link_cat_name: Name of the category as it is in the url.
    :param info_list_of_lists: The list of lists of book information
    in on category.
    """
    with open(
            pathlib.Path.cwd() / 'data' / link_cat_name /
            csv_name, 'w', newline='', encoding='utf-8-sig'
    ) as f:
        csv.writer(f).writerow([
            "product_page_url", "universal_product_code", "title",
            "price_including_tax", "price_excluding_tax",
            "number_available", "product_description", "category",
            "review_rating", "image_url", "saved_image_path"
        ])
        for info_list in info_list_of_lists:
            csv.writer(f).writerow(info_list)


def download_image(info_list, link_cat_name):
    """
    - Downloads the picture of one book from it's information list.
    - The name of the .jpeg file is created with the book name in the url.
    - The file is saved in a folder in /data named after
      the category's name in the url.

    :param info_list: The book information list.
    :param link_cat_name: Name of the category as it is in the url.
    """
    img = requests.get(info_list[-2])
    with open(
        pathlib.Path.cwd() / 'data' / link_cat_name / 'images' /
        f'{info_list[-1].replace(f"data/{link_cat_name}/images/", "")}',
        "wb"
    ) as i:
        i.write(img.content)


def elapsed_time_formatted(begin_time):
    """
    Calculates difference between begin_time and actual time,
    and formats it in HH:MM:SS.

    :param begin_time: time we want to compare with, in seconds.
    """
    return time.strftime(
        "%H:%M:%S", (time.gmtime(time.perf_counter() - begin_time))
    )


def entry_point():
    """
    This is the main job of BTS-Spy. Here is what it does:

    - Extract all categories url
    - initiate reference time
    - Initiate counters for the number of csv created (one per category)
      and books scraped
    - Prints a connexion confirmation and welcome message
    - Main loop: For each category:
        * Initiate reference time for the current category
        * keep current book counter
        * Define link_cat_name and csv name based upon it
        * Find all book links in a category
        * Show the category that is going to be scraped in console
        * Create folders to store category's files
        * Initiate list of lists of all books' information in the category
        * Launch the Child loop
          * Child loop: For each book in the category:
            ** Extract all information
            ** Append the list of all books' information
            ** Show progress in console
            ** Increase the book counter by one
            ** Download the picture
            ** Increase book_counter by one
        * Create the csv file with all books' information
        * Increase csv counter by one
        * Show success message with the amount books scraped in category
    - Show final success message with total amount of csv files
      and books scraped
    """
    # Extract all categories index url
    cat_index_urls = list_cat_index_urls("http://books.toscrape.com")

    begin_time = time.perf_counter()
    csv_counter = 0
    book_counter = 0

    print(
        "\nBTS_Spy connected successfully to http://books.toscrape.com !"
        "\nScrapping may take some time..."
        "\n\n####################################"
    )

    # Main loop
    for cat_index_url in cat_index_urls:
        begin_cat_time = time.perf_counter()
        previous_book_counter = book_counter

        link_cat_name = cat_index_url.replace(
            "http://books.toscrape.com/catalogue/category/books/", "").replace(
            "/index.html", "")
        csv_name = f'{link_cat_name}.csv'

        # Find all book links in a category
        links = list_book_links(list_pages_in_category(cat_index_url))

        print(
            "Processing with "
            f"{list_book_info(links[0], link_cat_name)[7]} category"
            "\n_________________________________________"
        )

        # Create folders to store category's files
        os.makedirs(
            pathlib.Path.cwd() / 'data' / link_cat_name / 'images', exist_ok=True
        )

        all_books_in_cat_info = []
        # Child loop
        for link in links:
            # Extract all information of one book
            book_info = list_book_info(link, link_cat_name)

            all_books_in_cat_info.append(book_info)

            download_image(book_info, link_cat_name)

            print(
                f"{book_counter} book(s) scraped | "
                f"Processing with book : {book_info[2]}"
            )

            book_counter += 1

        create_csv(csv_name, link_cat_name, all_books_in_cat_info)

        csv_counter += 1

        print(
            "___________________________________________________"
            "___________________________________________________"
            "___________________________________________________"
            f"\nOK ! Category n??{csv_counter} "
            f"with {book_counter - previous_book_counter} book(s) "
            f"inside entirely scraped | {link_cat_name}.csv "
            "successfully generated | "
            f"Processing time : {elapsed_time_formatted(begin_cat_time)} | "
            f"Total time : {elapsed_time_formatted(begin_time)}"
            "\n___________________________________________________"
            "___________________________________________________"
            "___________________________________________________"
        )

    print(
        f"Operation complete | {csv_counter} csv file(s) generated | "
        f"{book_counter} books scraped. | "
        f"Total time : {elapsed_time_formatted(begin_time)} | "
        "Goodbye !"
    )


if __name__ == '__main__':
    entry_point()
