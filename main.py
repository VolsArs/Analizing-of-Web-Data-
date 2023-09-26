import requests
from bs4 import BeautifulSoup, SoupStrainer
import json
from graphviz import Digraph
import os

#os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'
# создание файла страницы
# params = {'q': 'металлургическая промышленность в Российской Федерации'}
# url = 'https://duckduckgo.com/html/&'
#
headers = {"Accept": "*/*",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}

# req = requests.get(url, params=params, headers=headers)
#
# src = req.text
# print(src)
#
# with open('index.html', "w", encoding="utf-8") as file:
#     file.write(src)


# создание файла со ссылками json
# with open('index.html', encoding="utf-8") as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, 'html.parser')
# all_in_class = soup.find_all(class_='result__a')  # N54PNb BToiNc cvP2Ce
# all_links_dict = {}
# for item in all_in_class:
#     item_text = item.text
#     item_ref = 'https://' +item.get("href")
#
#     all_links_dict[item_text] = item_ref
#
#     print(item_text)
#     print(item_ref)
#
# with open ("all_links.json", "w", encoding="utf-8" ) as file:
#      json.dump(all_links_dict, file, indent=4, ensure_ascii=False)



list_of_nodesA = []
list_of_nodesB = []
with open("all_links.json", encoding="utf-8") as file:
    all_links = json.load(file)

for all_links_name, all_links_href in all_links.items():
    list_names = all_links_name
    list_href = all_links_href

    list_of_nodesA.append(all_links_name)
    list_of_nodesB.append(all_links_href)
    requests = requests.get(url=all_links_href, headers=)

    # print(list_of_nodesA)

for i in range(len(list_of_nodesB) - 1):
    rep = ["https://", "http://"]
    for item in rep:
        if item in list_of_nodesB[i]:
            list_of_nodesB[i] = list_of_nodesB[i].replace(item, (''))

print(list_of_nodesB)
g = Digraph('Mining_industry_sites', format='svg')

for i in range(len(list_of_nodesA) - 1):
        g.edge(list_of_nodesA[i], list_of_nodesB[i])

g.view()

###########

