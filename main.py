import time
from threading import Thread
import requests
from bs4 import BeautifulSoup
import sqlite3

# Задание. Парсинг сайта и Базы данных


def auto_parcing(page):
    url = f'https://auto.ria.com/search/' \
                    f'?indexName=auto,order_auto,newauto_search&' \
                    f'categories.main.id=1&' \
                    f'brand.id[0]=6&' \
                    f'country.import.usa.not=-1&' \
                    f'price.currency=1&' \
                    f'abroad.not=0&' \
                    f'custom.not=1&' \
                    f'photos.all.id.gte=1&' \
                    f'page={page}&' \
                    f'size=100'

    response = requests.get(url)
    if response.status_code == 200:
        adresses = []
        soup = BeautifulSoup(response.text, 'lxml')
            # для нахождения названий авто
        items_href = soup.find_all('a', class_='address', )
            # для нахождения цен на авто
            # items_price = soup.find_all('span', class_="bold size22 green", )

        for name in items_href:
            adresses.append(name.get('href'))

        threads_def = []
        for adress in adresses:
            t_def = Thread(target=auto_page(adress), args=(adress,))
            t_def.start()
            threads_def.append(t_def)

        for t_def in threads_def:
            t_def.join()


def auto_page(adress):
    url = adress
    response_auto = requests.get(url)
    if response_auto.status_code == 200:
        auto_soup = BeautifulSoup(response_auto.text, 'lxml')
        item_name = auto_soup.find('h1', class_="head",)
        # print(item_name)
        item_price = auto_soup.find('strong', class_="",)
        # print(item_price)
        item_mileage = auto_soup.find('div', class_="base-information bold",)
        # print(item_mileage)
        if item_name != None:
            auto_url.append(url)
            car_name.append(item_name.text)
            # print(item_name.text)
            prices.append(item_price.get_text())
            # print(item_price.get_text())
            mileage.append(item_mileage.get_text())
            # print(item_mileage.get_text())



dict = {}
prices = []
car_name = []
mileage = []
auto_url = []

start = time.perf_counter()
pages = 2  # в моем случае 78 страниц
for page in range(0, pages):
    auto_parcing(page)
end = time.perf_counter()
print(f'time = {end - start:0.2f} s')
print(len(car_name), len(mileage), len(prices), len(auto_url),)

dict = {}
adresses = []
prices = []
car_name = []
mileage = []
auto_url = []
threads = []

start = time.perf_counter()
pages = 2  # в моем случае 78 страниц
for page in range(0, pages):
    t = Thread(target=auto_parcing(page), args=(page,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
end = time.perf_counter()
print(f'time = {end - start:0.2f} s')

print(len(car_name), len(mileage), len(prices), len(auto_url),)

for i in range(0, len(car_name)):
      dict[f'Car number {i+1}'] = {
                    'Car name': car_name[i],
                    'Mileage': mileage[i],
                    'Price': prices[i],
                    'url': auto_url[i],
            }

# print(dict)
print(len(dict))

def create_table_auto(table: str, auto: dict):
    keys = ['ID']
    for k in auto['Car number 1'].keys():
        keys.append(k)
    values = ['Car number 1']
    for v in auto['Car number 1'].values():
        values.append(v)
    print(keys, values)

    create = f'CREATE TABLE {table}('
    for i in range(len(keys)):
        create += f'"{keys[i]}" "{values[i]}", '
    create = create[:-2] + ')'
    # print(create)
    connect = sqlite3.connect(f'{table}_data_base.db')
    cursor = connect.cursor()
    cursor.execute(create)
    connect.commit()


def iscert_table_auto(table: str, auto: dict):
    keys = ['ID']
    for k in auto['Car number 1'].keys():
        keys.append(k)
    # print(keys)
    # print(len(auto))
    for i in range(0, len(auto)):
        # print(i)
        values = [f'Car number {i+1}']
        for v in auto[f'Car number {i+1}'].values():
            values.append(v)
        # print(values)
        insert = f'INSERT INTO {table}' \
                 f'("{keys[0]}", "{keys[1]}", "{keys[2]}", "{keys[3]}", "{keys[4]}") ' \
                 f'VALUES ' \
                 f'("{values[0]}", "{values[1]}", "{values[2]}", "{values[3]}", "{values[4]}")'
        # insert = f'INSERT INTO {table} ' \
        #          f'("{keys[0]}", "{keys[1]}", "{keys[2]}", "{keys[3]}", "{keys[4]}") ' \
        #          f'VALUES ' \
        #          f'("Car number 2", "Audi Q5 2016", " 140 тис. км пробіг", "27 000 $", "https://auto.ria.com/uk/auto_audi_q5_33153625.html")'
        # print(insert)
        connect = sqlite3.connect(f'{table}_data_base.db')
        cursor = connect.cursor()
        cursor.execute(insert)
        connect.commit()


# создаем таблицу в БД
# create_table_auto('AUDI_autoria', dict)
# добавляем данные в БД
# iscert_table_auto('AUDI_autoria', dict)

def get_auto(table: str, auto: str):
    connect = sqlite3.connect(f'{table}_data_base.db')
    cursor = connect.cursor()
    get = f'SELECT "Car name", "Mileage", "Price", "url" FROM {table} WHERE ID="{auto}"'
    cursor.execute(get)
    result = cursor.fetchall()
    return result


# res = get_auto('AUDI_autoria', 'Car number 57')
# print(res)
