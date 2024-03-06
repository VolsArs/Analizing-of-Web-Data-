import pytesseract
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
from pdfminer.high_level import extract_pages, extract_text
from pypdf import PdfReader
import pdf2image
import requests
from bs4 import BeautifulSoup
import json
import os
import zipfile


def save_text_pdftext(filePath):
    reader = PdfReader(filePath)
    number_of_pages = len(reader.pages)
    my_file = open(r"E:\my_pdf\text_from_pdf.txt", "a",encoding="utf-8")
    for page in range(0, number_of_pages):
        current_page = reader.pages[page]
        text = current_page.extract_text()
        my_file.write(text)


def save_text_picture(filePath):
    pages = pdf2image.convert_from_path(filePath, dpi=200, size=(1654, 2340))
    my_file = open(r"E:\my_pdf\text_from_pdf.txt", "a", encoding="utf-8")
    for i in range(len(pages)):
        pages[i].save('E:\\spcs' + str(i) + '.jpg')
    text = pytesseract.image_to_string(pages[1], lang='rus')
    my_file.write(text)
    print(text)


def determine_type(filePath):
    for pagenum, page in enumerate(extract_pages(filePath)):
        for element in page:
            if isinstance(element, LTTextContainer):
                print('True')
                return True

            if isinstance(element, LTFigure):
                print('False')
                return False


def first_page(url, headers):
    url = url
    req = requests.get(url, headers=headers)
    src = req.text
    with open('index.html', "w", encoding="utf-8") as file:
        file.write(src)


def parsing_first_links():
    with open('index.html', encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, 'html.parser')
    menu_left = soup.find_all('a')
    all_links_dict = {}
    links_pdf_dict ={}
    for item in menu_left:
        item_text = item.get_text()
        item_href ="https://pstu.ru/" + str(item.get("href"))
        if (item_href[-4:] == '.pdf'):
            links_pdf_dict[item_text] = item_href
        else:
            all_links_dict[item_text] = item_href
        # print(item_href)
        # print(item_text)

    with open('all_links.json', "w", encoding="utf-8") as file:
        json.dump(all_links_dict, file, indent=4, ensure_ascii=False)
    with open('all_pdf.json', "w", encoding="utf-8") as file:
        json.dump(links_pdf_dict, file, indent=4, ensure_ascii=False)


def download_pdf():
    with open("all_pdf.json", encoding="utf-8") as file:
        all_pdf = json.load(file)
    links_pdf_dict = {}
    for links_names, links_href in all_pdf.items():
        links_pdf_dict[links_names] = links_href

    for value in links_pdf_dict.values():
        response = requests.get(value)
        print(value)
        if response.status_code == 200:
            file_path = os.path.join('E:\my_pdf',os.path.basename(value))
            with open(file_path, "wb") as file:
                file.write(response.content)


def iterating_files():
    directory = os.fsencode(r'E:\my_pdf')
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        path = str(directory)[2:12] +'\\'+str (filename)
        print(determine_type(path))
        if (determine_type(path)):
            save_text_pdftext(path)
        else:
            save_text_picture(path)
        print(path)


def zipping():
    file_zip = zipfile.ZipFile(r'E:\pdf.zip', 'w')
    for folder,subfolder,files in os.walk(r'E:\my_pdf\\'):
        for file in files:
            file_zip.write(os.path.join(folder, file),
            os.path.relpath(os.path.join(folder, file), 'E:\\'),
            compress_type = zipfile.ZIP_DEFLATED)
    file_zip.close()
    return file_zip


def sequance(url):
    headers = {"Accept": "*/*",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
    first_page(url, headers)

    parsing_first_links()
    for i in range(0, 2):

        with open('all_links.json', encoding="utf-8") as file:
            all_links = json.load(file)
        for links_names, links_href in all_links.items():
            req = requests.get(links_href, headers=headers)

            src = req.text

            with open('index.html', "w", encoding="utf-8") as file:
                file.write(src)

            with open('index.html', encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, 'html.parser')
            menu_left = soup.find_all('a')

            all_links_dict = {}
            links_pdf_dict = {}
            for item in menu_left:
                item_text = item.get_text()
                item_href = "https://pstu.ru/" + str(item.get("href"))
                if (item_href[-4:] == '.pdf'):
                    links_pdf_dict[item_text] = item_href
                else:
                    all_links_dict[item_text] = item_href

            with open('all_links.json', "w", encoding="utf-8") as file:
                json.dump(all_links_dict, file, indent=4, ensure_ascii=False)

            with open('all_pdf.json', encoding="utf-8") as file:
                old_pdf_dict = json.load(file)
            merged_dict = all_links_dict.update(old_pdf_dict)

            with open('all_pdf.json', "a", encoding="utf-8") as file:
                json.dump(merged_dict, file, indent=4, ensure_ascii=False)
    download_pdf()
    iterating_files()
    return zipping()


if __name__ == '__main__':
    sequance('https://pstu.ru/sveden/paid_edu')



