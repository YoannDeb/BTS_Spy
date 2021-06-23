# BTS_Spy

Projet d'études pour scraper le site d'entrainement [books.toscrape.com](http://books.toscrape.com).

Ceci est le projet n°2 de la formation [Open Classrooms](/https://openclassrooms.com) "DA Python".

Il est préférable d'avoir une version Python > 3.2.2 pour avoir un module html.parser correct.

## Création de l'environnement virtuel, téléchargement et execution du programme

Ouvrir un terminal, se placer dans le dossier voulu et lancer les commandes suivantes :

* Sur Linux ou Mac:
```
git clone https://github.com/YoannDeb/BTS_Spy.git
cd BTS_Spy
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python BTS_Spy.py
```

* Sur Windows:
```
git clone https://github.com/YoannDeb/BTS_Spy.git
cd BTS_Spy
python -m venv env
env\Scripts\activate.bat
pip install -r requirements.txt
python BTS_Spy.py
```

## Que fait ce programme ?
### Récupération d'informations :

Le programme va générer un fichier csv par catégorie, dans un dossier /data.
Le nom de ce fichier sera "nom_de_la_categorie_dans_url".csv.

Le séparateur csv est ",".

Le fichier contiendra ces entrées :
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


### Téléchargement des images des livres:

Le programme va également, dans le dossier data, créer un dossier pour chaque catégorie.

Le nom de ce dossier sera "nom_de_la_catégorie_dans_url"_img.

Dans ce dossier seront téléchargées toutes les images de tous les livres de chaque catégorie.
