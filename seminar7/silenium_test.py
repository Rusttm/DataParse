"""

    1 Выберите веб-сайт, который содержит информацию, представляющую интерес для извлечения данных. Это может быть новостной сайт, платформа для электронной коммерции или любой другой сайт, который позволяет осуществлять скрейпинг (убедитесь в соблюдении условий обслуживания сайта).
    2 Используя Selenium, напишите сценарий для автоматизации процесса перехода на нужную страницу сайта.
    3 Определите элементы HTML, содержащие информацию, которую вы хотите извлечь (например, заголовки статей, названия продуктов, цены и т.д.).
    4 Используйте BeautifulSoup для парсинга содержимого HTML и извлечения нужной информации из идентифицированных элементов.
    5 Обработайте любые ошибки или исключения, которые могут возникнуть в процессе скрейпинга.
    6 Протестируйте свой скрипт на различных сценариях, чтобы убедиться, что он точно извлекает нужные данные.
    7 Предоставьте ваш Python-скрипт вместе с кратким отчетом (не более 1 страницы), который включает следующее: URL сайта. Укажите URL сайта, который вы выбрали для анализа. Описание. Предоставьте краткое описание информации, которую вы хотели извлечь из сайта. Подход. Объясните подход, который вы использовали для навигации по сайту, определения соответствующих элементов и извлечения нужных данных. Трудности. Опишите все проблемы и препятствия, с которыми вы столкнулись в ходе реализации проекта, и как вы их преодолели. Результаты. Включите образец извлеченных данных в выбранном вами структурированном формате (например, CSV или JSON). Примечание: Обязательно соблюдайте условия обслуживания сайта и избегайте чрезмерного скрейпинга, который может нарушить нормальную работу сайта.



"""

import json
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

DELAY_TIME = 3

options = Options()
# not open browser
# options.add_argument('headless')
options.add_argument('window-size=1200x600')
driver = webdriver.Chrome(options=options)

driver.get("https://for-est.ru/")
# выбираем город Москва
city_choose_line = "//div[contains(@class, 'region_wrapper')]//*[name()='use' and @*='#i-angle']"
city_slider = driver.find_element(By.XPATH, city_choose_line)
city_slider.click()
time.sleep(DELAY_TIME)
moscow_choose_line = "//a[contains(@href, '/?region=5478')]"
moscow_choose = driver.find_element(By.XPATH, moscow_choose_line)
moscow_choose.click()
time.sleep(DELAY_TIME)
# переходим на страницу с инструментами
open_inst_page = driver.find_element(By.XPATH, "//a[@href='/catalog/instrument/' and @class='left-catalog__link parent']")
# (//a[@class='left-catalog__link parent'])[4]
open_inst_page.click()
# открываем еще одну страницу
open_next_page = driver.find_element(By.XPATH, "//div[@class='ajax_load_btn']")
open_next_page.click()
time.sleep(DELAY_TIME)
instruments_titles = driver.find_elements(By.XPATH, "//a[@class='dark_link']/span")
instruments_prices = driver.find_elements(By.XPATH, "//span[@class='price_value']")
result_list = []
for i, elem in enumerate(instruments_titles):
    inst_title = instruments_titles[i].text
    inst_price = str(instruments_prices[2*i].text).replace(" ", "")
    # inst_price = int(str(elem.text).replace(" ", ""))
    result_list.append({"title": inst_title, "price": inst_price})
    print(f"{inst_title}:{inst_price}")
driver.save_screenshot('screen.png')
driver.quit()

if len(result_list) > 0:
    keys = result_list[0].keys()
    with open("instruments_price.csv", "w", newline="") as file:
        w = csv.DictWriter(file, keys)
        w.writeheader()
        w.writerows(rowdicts=result_list)