import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime, time, timedelta
import time
import re
import json
import pandas as pd
from tqdm import tqdm

# Запрос веб-страницы


# Парсинг HTML-содержимого веб-страницы с помощью Beautiful Soup

def parse_prod_descr(prod_href) -> str:
    """ get href /its-only-the-himalayas_981/index.html"""
    prod_url = 'http://books.toscrape.com/catalogue' + prod_href
    response = requests.get(prod_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    p_list = soup.find('article', {'class': 'product_page'}).find_all('p')
    description = p_list[3].get_text()
    time.sleep(1)
    return description
def parse_page(page_url) -> tuple:
    """ get url 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html'"""
    prod_list = []
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for prod_card in soup.find_all('article', {'class': 'product_pod'}):
        prod_name = prod_card.find('h3').find('a').get('title')
        prod_price = prod_card.find('p', {'class': 'price_color'}).text
        prod_price = float(prod_price.replace('£', ''))
        prod_av = prod_card.find('p', {'class': 'instock availability'}).text
        prod_av = re.sub('[^A-Za-z0-9]+', '', prod_av)
        # prod_av = ''.join(filter(str.isalnum, prod_av))

        prod_href = prod_card.find('h3').find('a').get('href')
        prod_href = prod_href.split('..')[-1]
        prod_descr = parse_prod_descr(prod_href)
        # prod_list.append((prod_name, prod_price, prod_av, prod_descr))
        prod_list.append({"book_title": prod_name, "book_price": prod_price, "book_stock": prod_av, "book_description": prod_descr})
    next_page_href = soup.find('li', {'class': 'next'})
    if next_page_href:
        next_page_href = next_page_href.find('a').get('href')
        # next_page_href = '/'.join(page_href.split('/')[:-1]) + '/' + next_page_href
    return prod_list, next_page_href

def parse_category(cat_href: str) -> list:
    """ gets href like 'catalogue/category/books/mystery_3/index.html' """
    all_cat_prod_list = []
    next_href = cat_href
    for i in range(10):
        prod_list, next_href = parse_page(next_href)
        all_cat_prod_list.extend(prod_list)
        if next_href:
            next_href = '/'.join(cat_href.split('/')[:-1]) + '/' + next_href
        else:
            break
    return all_cat_prod_list

def write_csv(data_list):
    df = pd.DataFrame(data_list, columns=["prod_name", "prod_price", "prod_stock", "prod_description"])
    df.to_csv('result.csv', index=False)
    print(df)

def write_json(data_list):
    with open("result.json", "w") as file:
        json.dump(data_list, file)




def main():
    all_prod_list = []
    categories_hrefs = []
    url = 'http://books.toscrape.com/'
    additional_href = '/catalogue/category/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    categories = soup.find('ul', ('class', 'nav nav-list')).find('li').find('ul').find_all('li')
    # for category in categories:
    list_len = len(categories)
    for i in tqdm(range(list_len)):
        category = categories[i]
        try:
            href = category.find('a').get('href')
        except Exception as e:
            print(f"cannot parsing, error: {e}")
        else:
            cat_href = url + href
            all_prod_list.extend((parse_category(cat_href)))
    print(all_prod_list)
    # write_csv(all_prod_list)
    write_json(all_prod_list)



if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f"Parsed in {round(time.time() - start_time, 2)}sec.")
