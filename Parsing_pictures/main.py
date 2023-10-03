import requests
from bs4 import BeautifulSoup, SoupStrainer
import os
import zipfile


def get_pictures(url):
    url = url  #'https://scryfall.com/search?q=(e%3Altr+cn%3E%3D452)+or+(e%3Altc+cn%3E%3D411)&order=set&as=grid&unique=prints'

    headers = {"Accept": "*/*",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}

    req = requests.get(url, headers=headers)

    src = req.text

    with open('index.html', "w", encoding="utf-8") as file:
        file.write(src)

    with open('index.html', encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'html.parser')
    all = soup.find_all(class_="card ltc border-black")

    count = 0
    file_zip = zipfile.ZipFile(r'D:\pic.zip', 'w')
    for item in all:
        count+=1
        item_url = item.get("src")
        print(item_url)
        image = requests.get(item_url).content
        with open(r'D:\pic\\' + str(count)+'.jpg', 'wb')as handler:
            handler.write(image)

    for folder,subfolder,files in os.walk(r'D:\pic\\'):
        for file in files:
            if file.endswith('.jpg'):
                file_zip.write(os.path.join(folder, file),
                os.path.relpath(os.path.join(folder, file), 'D:\\'),
                compress_type = zipfile.ZIP_DEFLATED)
    file_zip.close()
    return file_zip

get_pictures('https://scryfall.com/search?q=(e%3Altr+cn%3E%3D452)+or+(e%3Altc+cn%3E%3D411)&order=set&as=grid&unique=prints')
