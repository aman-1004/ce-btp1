import pandas as pd
from imdrain import ImdRain

df = pd.read_csv('combined.csv').dropna()
a = ImdRain(2019, 2022)

for index, entry in df.iterrows():
    lat = ImdRain.degree_to_decmial(entry['lat'])
    long = ImdRain.degree_to_decmial(entry['long'])
    date = entry['date']
    res = a.get_n_days_data(5, date, lat, long)
    # print(date, lat, long, *res, sep=',')


# res = a.get_n_days_data(5, '2022-07-19', 33.15, 77)
# print(res)

