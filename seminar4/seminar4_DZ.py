# -*- coding: utf-8 -*-

# Импорт необходимых библиотек
import requests
from lxml import html
import pandas as pd
import csv

# Определение целевого URL
url = "https://cbr.ru/currency_base/daily/"

# Отправка HTTP GET запроса на целевой URL с пользовательским заголовком User-Agent
response = requests.get(url, headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
# Парсинг HTML-содержимого ответа с помощью библиотеки lxml
tree = html.fromstring(response.content)


def exchange_course(tree) -> pd.DataFrame:
    df = pd.DataFrame()
    try:
        # Использование выражения XPath для выбора всех строк таблицы в пределах таблицы с классом 'records-table'
        table_rows = tree.xpath(".//table[@class='data']/tbody")
        table_columns = table_rows[0].xpath("./tr//th/text()")
        # Использование выражения XPath для выбора всего текстового содержимого элементов 'td' в первой строке таблицы
        rows = table_rows[0].xpath(".//tr[position() > 1]")
    except Exception as e:
        print(f"Cant parse tree for exchange course, error: {e}")
    else:
        # Запись даных в файл csv
        data_rows = [row.xpath(".//td/text()") for row in rows]
        df = pd.DataFrame(data_rows, columns=table_columns)
        df.to_csv("exchange.csv")
        print("file 'exchange.csv' successfully saved")
    return df


exchange_course(tree)
