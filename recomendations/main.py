import requests
from bs4 import BeautifulSoup
import lxml.html
import pandas as pd
import numpy as np
import openpyxl
import seaborn as sns
from scipy.sparse import csr_matrix
from sklearn.metrics import accuracy_score
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()



00


def make_database():
    # url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    #
    # headers = {"Accept": "*/*",
    #            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
    #
    # req = requests.get(url, headers=headers)
    #
    # src = req.text
    #
    #
    # with open('index_.html', "w", encoding="utf-8") as file:
    #     file.write(src)

    with open('index_.html', encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'html.parser')


    all_in_class = soup.find_all(class_="ipc-title__text")
    names = []
    ratings = []
    for item in all_in_class:
        for i, leter in enumerate(str(item.text)):
            if leter == '.':
                name = item.text[i+1:].lstrip()

                names.append(name)
                break


    all_ratings = soup.find_all(class_='sc-c7e5f54-1 byLSsq')
    for item in all_ratings:
        rating = item.text[0:4]
        ratings.append(rating)
    print(str(len(names))+' names')
    print(str(len(ratings))+' ratings')


    df = pd.DataFrame(names,columns=['NAME'])
    df['RATING'] = ratings
    print(df)
    df.to_excel(r'D:\Learn\2.Kurs\3 Semestr\WebDataMining\recomendations\films_library.xlsx')
    return df

#make_database()

def knn():
    file1 = 'my_rating.xlsx'
    my_ratings = pd.ExcelFile(file1)
    my_df = my_ratings.parse('Лист1')

    file2 = 'films_library.xlsx'
    film_library = pd.ExcelFile(file2)
    films_lib_df = film_library.parse('Sheet1', index_col=0)

    X_train = my_df.drop('NAME', axis=1)
    #y_train = my_df['NAME']

    X_test = films_lib_df.drop('NAME', axis=1)
    #y_test = films_lib_df['NAME']

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    #for classifications
    #knn = KNeighborsClassifier(n_neighbors=10)
    #knn.fit(X_train, y_train)
    #Создание модели
    knn = NearestNeighbors(n_neighbors=9, algorithm='ball_tree').fit(X_train)

    # определение дистанциий и индексов
    distances, indices = knn.kneighbors(X_test)

    # создание листов
    indices_list = indices.squeeze().tolist()
    distances_list = distances.squeeze().tolist()

    # создани кортежа из индексов и дистанции
    indices_distances = list(zip(indices_list, distances_list))
    print(type(indices_distances[0]))
    # сортировка кортежа и взять первый элемент
    indices_distances_sorted = sorted(indices_distances, key=lambda x: x[1], reverse=False)
    finish_tuple = indices_distances_sorted[:1]

    # создание отдельного списка индексов
    finish_indexes = []
    for elem in finish_tuple:
        for element in elem:
            for i, y in enumerate(element):
                print(i, y)
                finish_indexes.append(y)
                if i == 8:
                    break
            break

    # получние списка фильмов с названиями
    var = films_lib_df.iloc[finish_indexes]
    print(var)


knn()