import requests
from bs4 import BeautifulSoup, SoupStrainer
import json
import numpy
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


cities = ['Перми', 'Москвы', 'Санкт-Петербург']



def get_data(cities):

    asian = {'лапша': 0, 'фунчоза': 0, 'том.ям': 0, 'суши': 0, 'роллы': 0}
    gergian = {'хачапури': 0, 'хинкали': 0, 'чахохбили': 0, 'долма': 0, 'чашушули': 0}
    italian = {'лазанья': 0, 'минестроне': 0, 'карпаччо': 0, 'пицца': 0, 'паста': 0}
    cuisines = [asian, gergian,italian]
    count_cities = 0

    data_for_df = [asian, gergian,italian]

    df = pd.DataFrame(data_for_df, index=['Перми', 'Москвы', 'Санкт-Петербург'])
    df = df.fillna(0)

    print(df)


    for city in cities:

        url = 'https://www.google.ru/search?q'
        text_of_query = f"Популярные блюда в ресторанах и кафе {city} СМИ"

        params = {'q': text_of_query}

        headers = {"Accept": "*/*",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}

        req = requests.get(url, params=params, headers=headers)

        src = req.text


        with open(f'index_{count_cities}.html', "w", encoding="utf-8") as file:
            file.write(src)

        with open(f'index_{count_cities}.html', encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, 'html.parser')
        all_links_dict = {}

        for result in soup.select('.tF2Cxc'):
            link = result.select_one('.yuRUbf a')['href']
            print(link, sep='\n')
            text = result.select_one('.yuRUbf h3').text
            print(text, sep='\n')
            all_links_dict[text] = link


        with open (f"links_{count_cities}.json", "w", encoding="utf-8" ) as file:
            json.dump(all_links_dict, file, indent=4, ensure_ascii=False)


        with open(f"links_{count_cities}.json", encoding="utf-8") as file:
            links = json.load(file)

        # top_one = ''
        # top_one_number = list(cuisines[0].values())[0]
        dict_top = {}
        count_cousines = 0


        for cuisine in cuisines:

            # определение текста сайта из списка ссылок
            for all_links_name, all_links_href in links.items():
                list_href = all_links_href
                req = requests.get(url=all_links_href, headers=headers)
                src = req.text.lower()
                print(all_links_href)
                data_keys = cuisine.keys()

                # поиск и подсчет значений в тексте сайта
                for key in data_keys:
                    print(key+": " + str(cuisine.get(key)))
                    count = src.count(key)
                    print(count)
                    cuisine.update({key: cuisine.get(key) + count})

            top_one = ''
            top_one_number = 0
            # выявление самого часто упоминаемого блюда
            data_keys = cuisine.keys()
            for key in data_keys:
                print(top_one)
                if cuisine.get(key) > top_one_number:
                    top_one_number = cuisine.get(key)
                    top_one = key
                    dict_top.clear()
                    #print(dict_top)
                    dict_top.update({key: top_one_number})

                cuisine.update({key: 0})


            count_cousines += 1
            print(cuisine)
            df.at[cities[count_cities], top_one] = 1
            print(f'Самое часто упоминаемое блюда в СМИ {cities[count_cities]}'+ " - " + str(top_one) + " упоминатеся в СМИ " + str(top_one_number)+ " раз")
            print(df)
            # with open(f"City_{count_cities}_cousines_{str(count_cousines)}.json", "w", encoding="utf-8" ) as file:
            #     json.dump(dict_top, file, indent=4, ensure_ascii=False)
        count_cities += 1

    df.to_excel(r'D:\Learn\2.Kurs\3 Semestr\WebDataMining\cuisines\mydata.xlsx')



def k_means():
    file = 'mydata.xlsx'
    xl = pd.ExcelFile(file)
    df = xl.parse('Sheet1')
    df.drop(df.columns[[0]], axis=1, inplace=True)
    print(df)
    X = df.to_numpy()
    print(X)
    scaler = StandardScaler()
    scaled_df_kmeans = scaler.fit_transform(df)
    kmeans_model = KMeans(n_clusters=3)
    #clusters = kmeans_model.fit(df)
    kmeans_model.fit(X)
    print(kmeans_model.cluster_centers_)
    print(kmeans_model.labels_)
    plt.scatter(X[:, 0], X[:, 1], c=kmeans_model.labels_, cmap='rainbow')

    plt.scatter(kmeans_model.cluster_centers_[:, 0], kmeans_model.cluster_centers_[:, 1], color='black')


    #df.insert(df.columns.get_loc("лапша"), "Cluster", clusters)
    df.head(3)
    ssd = []
    for k in range(2, 4):
        kmeans_model = KMeans(n_clusters=k)
        kmeans_model.fit(df)
        ssd.append(kmeans_model.inertia_)
    plt.figure(figsize=(6, 4), dpi=100)
    plt.plot(range(2, 4), ssd, color="green", marker="o")
    plt.xlabel("Number of clusters (K)")
    plt.ylabel("SSD for K")
    plt.show()


def main():
    get_data(cities)
    k_means()

if __name__ == "__main__":
    main()

