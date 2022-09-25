import time
from threading import Thread
import requests
from bs4 import BeautifulSoup

# Задание. Парсинг сайта


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
    auto_url.append(url)
    response_auto = requests.get(url)
    if response_auto.status_code == 200:
        auto_soup = BeautifulSoup(response_auto.text, 'lxml')
        item_name = auto_soup.find('h1', class_="head",)
        car_name.append(item_name.text)
        # print(url)
        # print(item_name.text)
        item_price = auto_soup.find('strong', class_="",)
        prices.append(item_price.get_text())
        # print(item_price.get_text())
        item_mileage = auto_soup.find('div', class_="base-information bold",)
        mileage.append(item_mileage.get_text())
        # print(item_mileage.get_text())



dict = {}
adresses = []
prices = []
car_name = []
mileage = []
auto_url = []
threads = []


# так и не понял как вытянуть из автория количество страниц.
# такое ощущение что там то ли защита стоит,
# то ли как-то по другому надо дааные получать,
# т.к. постоянно получал пустые данные
start = time.perf_counter()
pages = 78  # в моем случае 78 страниц
for page in range(0, pages):
    t = Thread(target=auto_parcing(page), args=(page,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
    
end = time.perf_counter()
print(f'time = {end - start:0.2f} s')

# print(len(car_name), len(mileage), len(prices), len(auto_url),)

for i in range(0, len(car_name)):
      dict[f'Car number {i+1}'] = {
                    'Car name': car_name[i],
                    'Mileage': mileage[i],
                    'Price': prices[i],
                    'url': adresses[i],
            }

print(dict)


