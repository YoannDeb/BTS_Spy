# BTS_Spy

Training Project to scrape some information on training site [books.toscrape.com](http://books.toscrape.com).

Part of [Open Classrooms](/https://openclassrooms.com) "DA Python" formation, 2nd Project.

It's better to have Python > 3.2.2 for decent html.parser.

## Creating Virtual environment, downloading and running the program

You need Python (minimum 3.2.2, tested on 3.9.5) and git installed on your machine. 
Open a terminal and navigate into the folder you want BTS-Spy to be downloaded, and run the following commands:

* On Linux or MacOS:
```
git clone https://github.com/YoannDeb/BTS_Spy.git
cd BTS_Spy
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python BTS_Spy.py
```

* On Windows:
```
git clone https://github.com/YoannDeb/BTS_Spy.git
cd BTS_Spy
python -m venv env
env\Scripts\activate.bat
pip install -r requirements.txt
python BTS_Spy.py
```

## What is this program doing?
### Information retrieving:

It will generate one csv file by category, whose name is "category_url_name".csv, in a folder /data/"category_url_name".

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
 
Also downloaded all images of all the books in each category, in a folder data/"category_url_name"/images.
