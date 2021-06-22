# BTS_Spy

Training Project to scrape some information on training site [books.toscrape.com](http://books.toscrape.com)

Part of [Open Classrooms](/https://openclassrooms.com) "DA Python" formation, 2nd Project

It's better to have Python > 3.2.2 for decent html.parser

## Creating Virtual environment, downloading and running the program

Open a terminal and navigate into the folder you want BTS-Spy to be downloaded, and run the following commands:

```
git clone https://github.com/YoannDeb/BTS_Spy.git
cd BTS_Spy
Python -m venv env
source env/bin/activate
pip install -r requirements.txt
Python BTS_Spy.py
```

## What is this program doing?
### Information retrieving:

It will generate one csv file by category, whose name is "category_url_name".csv, in a folder /data  

The separator in the csv file is ",".

This file will contain those entries :
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
- saved_image_path


### Book image downloading:
 
Also creates an image folder for each category, whose name will be "category_url_name"_img.

In this folder will be downloaded all images of all the books of one category.
