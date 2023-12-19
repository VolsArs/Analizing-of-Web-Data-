import json
import requests
import urllib.request
from bs4 import BeautifulSoup

wiki_request = 'http://ru.wikipedia.org/w/api.php?action=query&list=search&srsearch=Металлургия=%20России&format=json'

headers = {"Accept": "*/*",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
subject = 'Металлургия России'

url = 'https://ru.wikipedia.org/w/api.php'
session = requests.Session()

def get_text():
    params = {
        'action': 'parse',
                'page': subject,
                'format': 'json',
                'prop':'text',
                'redirects':''
    }



    #response = session.get(url=url, params=params)
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    #print(data)
    #pages = data["query"]["pages"]

    raw_html = data['parse']['text']['*']

    with open("content_req.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


    soup = BeautifulSoup(raw_html,'html.parser')
    soup.find_all('p')
    text = ''

    for p in soup.find_all('p'):
        text += p.text
        print(text)

    print(text[:58])
    print('Text length: ', len(text))

def get_links():
    params = {
        'action': 'parse',
        'page': subject,
        'format': 'json',
        'prop': 'text',
        'redirects': ''
    }

    response = requests.get(url, params=params)
    data = response.json()

    raw_html = data['parse']['text']['*']
    soup = BeautifulSoup(raw_html, 'html.parser')
    h = soup.find_all('p')
    print(h)

    text = ''



    for p in soup.find_all('href'):
        text += p.text
        print(text)

get_text()

get_links()
