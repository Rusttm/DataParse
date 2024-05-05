# -*- coding: utf-8 -*-

# Импорт необходимых библиотек
import requests
from lxml import html
import pandas as pd
import csv
from datetime import datetime
import random

list_user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188 ",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0 ",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
]

def exchange_course(tree) -> pd.DataFrame:
    """parses table of exchange courses in csv file"""
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
    return df


def get_date() -> datetime.date:
    """ returns date after input, or today date"""
    res_date = datetime.now()
    date_req = input("Введите дату в формате 21.12.2022 (Ввод -пропустить): ")
    try:
        res_date = datetime.strptime(date_req, "%d.%m.%Y")
        if res_date.date() > datetime.now().date():
            raise ValueError(f"Можно посмотреть курс только до сегодняшнего дня: {res_date.date()}")
    except Exception as e:
        print(f"Ошибка ввода даты, error: {e}")
        print(f"Собираю курсы на сегодня: {res_date.date()}")
    return res_date


def exchange_course_on_date():
    """ saves table of courses on date in csv table """
    req_date = get_date()
    date_str = req_date.strftime("%d.%m.%Y")
    try:
        # Определение целевого URL
        url = f"https://cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To={date_str}"
        # Отправка HTTP GET запроса на целевой URL с пользовательским заголовком User-Agent
        response = requests.get(url, headers={'User-Agent': random.choice(list_user_agents)})
        if 200 <= response.status_code <300:
            print("данные с сайта запрошены")
        # Парсинг HTML-содержимого ответа с помощью библиотеки lxml
        tree = html.fromstring(response.content)
        result_df = exchange_course(tree)
    except Exception as e:
        print(f"cant parse site, error {e}")
    else:
        file_name = f"exchange_{req_date.strftime('%d_%m_%y')}.csv"
        result_df.to_csv(file_name)
        print(f"Данные успешно записаны в файл '{file_name}'")


if __name__ == '__main__':
    exchange_course_on_date()
