# requests - библиотека помогает нам работать с http запросами
# bs4 - библиотека позваоляет нам извлекать информацию из html
# данная библиотека разбирается в тегах, различает от обычного текста
# она может извлекать данные из нужных тегов


import requests
from bs4 import BeautifulSoup as BS
import csv


def get_html(url: str) -> str:
    response = requests.get(url)
    return response.text

def get_data(html):
    soup = BS(html, 'lxml')
    catalog = soup.find('div', class_='catalog-list')
    cars = catalog.find_all('a', class_='catalog-list-item')
    ind = 0
    for car in cars:
        params = car.find('span', 'catalog-item-params')
        try:
            title = car.find('span', class_='catalog-item-caption').text.strip()
            ind = title.index(',')
            title = title[:ind]
        except:
            title = "Название не указано"
        
        try:
            price = car.find('span', class_='catalog-item-price').text.strip()
        except:
            price = 'Цена не указана'

        try:
            img = car.find('img', class_='catalog-item-cover-img').get('src')
        except:
            img = 'Пустое фото'

        try:
            descr = car.find('span', class_='catalog-item-descr').text.strip()
        except:
            descr = 'Описания нету'

        try:
            date = car.find('span', class_='catalog-item-info').text.strip()
        except:
            data = 'Даты нету'

        try:
            milit = params.find('span', 'catalog-item-mileage').text.strip()
        except:
            milit = "Пробег не указан"

        data = {
            'title': title,
            'price': price,
            'image': img,
            'descr': descr,
            'date': date,
            'mileage': milit
        }
        write_csv(data)
        

def write_csv(data: dict) -> None:
    with open('cars.csv', 'a') as csv_file:
        fieldnames = ['title', 'price', 'image', 'descr', 'date', 'mileage']
        writer = csv.DictWriter(csv_file, delimiter='/', fieldnames=fieldnames)
        writer.writerow(data)


def main():
    # url = 'https://cars.kg/offers'
    # html = get_html(url)
    # data = get_data(html)

    for page in range(1, 21):
        url = f'https://cars.kg/offers/{page}'
        print(f'Парсинг {page} страницы!')
        html = get_html(url)
        get_data(html)
        print(f'Парсинг {page} страницы завершен!')
    


