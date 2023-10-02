import pandas as pd
import matplotlib.pyplot as plt
import folium

# define the world map
russia_map = folium.Map(
    location=[64.6863136, 97.7453061],
    zoom_start=4
)


# импортируем dataframe
df = pd.read_csv(r'D:\Learn\2.Kurs\3 Semestr\WebDataMining\lab2\museum.csv')
muz = df[['Название','Местоположение', 'На карте','Адрес']]

df['Координаты'] = df['На карте'].str.rstrip(':').str.split(':').str[2]

coordinates = []
list = []
for column in df:
    columnSeriesObj = df['Координаты']
    list = columnSeriesObj.values.tolist()


for item in list:
    one_coord = []
    str_shir = str(item)

    com = str_shir.index(',')
    dolg = str_shir[1:com]
    shir = str_shir[com+1:len(str_shir)-2]
    one_coord = [float(shir), float(dolg)]
    coordinates.append(one_coord)
        #print("Ширина Долгота  " + shir + '   ' +dolg)
        #folium.Marker([44.097006, 39.071505], icon=folium.Icon(color="green")).add_to(russia_map)
        #folium.Marker([float(shir), float(dolg)], icon=folium.Icon(color="green")).add_to(russia_map)
#
print(len(coordinates))
for item in range(len(coordinates)):
    folium.Marker(coordinates[item], icon=folium.Icon(color="green")).add_to(russia_map)


russia_map.save(r'D:\Learn\2.Kurs\3 Semestr\WebDataMining\lab2\map.html')

df['Регион'] = df['Адрес'].str.rstrip(',').str.split(',').str[0]


#Counting unique regions
uniq = df['Регион'].value_counts()

df_uniq= pd.DataFrame(uniq)
df_uniq= df_uniq.reset_index()
df_uniq.columns = ['unique_values', 'counts']



#Plot bars
fig = plt.figure(figsize=(40, 14), dpi=96)
ax = fig.add_subplot()

ax.bar(df_uniq['unique_values'], df_uniq['counts'], width=0.2)

plt.xticks(rotation=90)
ax.grid()

plt.show()
plt.savefig(r'D:\Learn\2.Kurs\3 Semestr\WebDataMining\lab2\graf.png')

