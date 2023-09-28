import requests

from bs4 import BeautifulSoup, SoupStrainer
import json
from graphviz import Digraph
import os
import spacy
from spacy.matcher import Matcher
import spacy.cli
from spacy.lang.ru import Russian

# spacy.cli.download("ru_core_news_sm")
# nlp = Russian()
nlp = spacy.load("ru_core_news_lg")
matcher = Matcher(nlp.vocab)
pattern1 = [
    [{'LOWER': 'цветная'}]
]

os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'
# создание файла страницы

url = 'https://www.google.ru/search?q'
params = {'q': 'металлургическая промышленность в Российской Федерации'}

headers = {"Accept": "*/*",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}

req = requests.get(url, params=params, headers=headers)

src = req.text


with open('index.html', "w", encoding="utf-8") as file:
    file.write(src)


#создание файла со ссылками json
with open('index.html', encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, 'html.parser')
all_in_class = soup.find_all(class_="yuRUbf")            #N54PNb BToiNc cvP2Ce
all_links_dict= {}
for item in all_in_class:

    item_url = item.get("h3")
    print(item_url)
    item_text = item.get("h3")
    print(item_text)

    item_ref = 'https:'+ item.get("href")

    all_links_dict[item_text] = item_ref


with open ("all_links.json", "w", encoding="utf-8" ) as file:
     json.dump(all_links_dict, file, indent=4, ensure_ascii=False)


with open("all_links.json", encoding="utf-8") as file:
    all_links = json.load(file)



def connection(maches):
    if maches:
        if maches[0][0] != 0:
            return True
        else:
            return False
    else:
        return False



g = Digraph('Mining_industry_sites', format='svg')
rep = ["https://", "http://"]
for all_links_name, all_links_href in all_links.items():
    list_href = all_links_href
    req = requests.get(url=all_links_href, headers=headers)
    src = req.text
    matcher.add('4M', pattern1)
    doc = nlp(src)

    maches = matcher(doc)

    if connection(maches):
        for item in rep:
            if item in all_links_href:
                all_links_href = all_links_href.replace(item, (''))
                g.edge(str(pattern1[0][0]['LOWER']), all_links_href)



g.view()

###########
