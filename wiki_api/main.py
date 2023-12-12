import wikipedia
import json
import requests
import urllib.request

wiki_request = 'http://ru.wikipedia.org/w/api.php?action=query&list=search&srsearch=Металлургия=%20России&format=json'

subject = 'Металлургия России'

url = 'https://ru.wikipedia.org/w/api.php'
session = requests.Session()

params = {
    "action": "query",
    "format": "json",
    "titles": subject,
    "prop": "links",
    "pllimit": "max"
}

response = session.get(url=url, params=params)
data = response.json()
pages = data["query"]["pages"]

pg_count = 1
page_titles = []

print("Page %d" % pg_count)
for key, val in pages.items():
    for link in val["links"]:
        print(link["title"])
        page_titles.append(link["title"])

while "continue" in data:
    plcontinue = data["continue"]["plcontinue"]
    params["plcontinue"] = plcontinue

    response = session.get(url=url, params=params)
    data = response.json()
    pages = data["query"]["pages"]

    pg_count += 1

    print("\nPage %d" % pg_count)
    for key, val in pages.items():
        for link in val["links"]:
            print(link["title"])
            page_titles.append(link["title"])

print("%d titles found." % len(page_titles))


def get_links():
    links_dict = {}
    wikipedia.set_lang("ru")
    links_list = wikipedia.page("Металлургия России").references
    count = 0
    for link in links_list:
        print(link)
        links_dict[count] = link


    with open("content.json", "w", encoding="utf-8") as file:
        json.dump(links_dict, file, indent=4, ensure_ascii=False)


def get_text():
    wikipedia.set_lang("ru")
    text = wikipedia.page("Металлургия России").content

    with open('text.txt', "w", encoding="utf-8") as file:
        file.write(text)


def get_image():
    image_links = []
    try:
        for i in range(20):
            image_links.append(wikipedia.page("Металлургия России").images[i])
    except Exception as e:
        print(e)
    finally:
        count = 0
        for link in image_links:
            print(link)
            resource = urllib.request.urlopen(link)
            out = open(r'D:\pic\\' + str(count) + '.jpg', 'wb')
            out.write(resource.read())
            out.close()
            count += 1


def main():
    get_links()
    get_text()
    get_image()


if __name__ == "__main__":
    main()
