import time
from random import randrange
import openpyxl
import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from sqlalchemy import create_engine

executable_path = "C:/chromedriver.exe"
service = ChromeService(executable_path=executable_path)
driver = webdriver.Chrome(service=service)

id_names = ["hyperlinkDrivetechnology", "hyperlinkAutomationtechnology", "hyperlinkEnergy", "hyperlinkBuildingTechnologies", "hyperlinkSafetySystems-SafetyIntegrated", "hyperlinkMarket-specificsolutions", "hyperlinkDigitalEnterpriseServices"]

# подготавливаем заголовки для отправки запросов
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0 (Edition Yx GX)"
}
# инициализируем списки различных собираемых данных
urls = []
id_nums = []

# посылаем запрос на стартовую страницу и собираем ссылки родительских категорий

with requests.Session() as s:
    response = s.get(url="https://mall.industry.siemens.com/mall/en/ru/Catalog/Products/1000000", headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    for name in id_names:
        title_url = soup.find('a', id=f'{name}')
        urls.append(title_url.get('href'))
    urls.append("https://mall.industry.siemens.com/mall/en/ru/Catalog/Products/9990314")

# запускаем цикл итерации всех родительских ссылок для получения первой развертки древа категорий
for url in urls:
    # из ссылок полученных ранее достаем айди страницы, чтобы можно было находить конкретные элементы на странице
    id_num = url.split('/')[-1]
    response = s.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    # находим нужные элементы
    branch = soup.find('a', id=f"{id_num}").find_next('div', class_="PopupItems").find_all('a', class_="internalLink")
    # итерируем найденные элементы и пополняем изначальный список значениями которых там еще нет
    for item in branch:
        id_num = item.get('href').split("/")[-1]
        id_nums.append(id_num)


logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
product_pages = []
# запускаем цикл итерации всех ссылок категорий древа, список id_nums пополняется новыми данными по мере прохождения
# цикла, конечные ссылки записываем в txt файл при каждой итерации если они есть в данной итерации цикла
for id_num in id_nums:
    # запускаем проверку на дальнейшее разворачивания древа
    try:
        url = f"https://mall.industry.siemens.com/mall/en/ru/Catalog/Products/{id_num}?tree=CatalogTree"
        s = requests.Session()
        response = s.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        branch = soup.find('div', class_="Item").find_next('a', id=f"{id_num}").find_next('div', class_="PopupItems").find_all('a', class_="internalLink")
        for item in branch:
            id_num = item.get('href').split("/")[-1]
            if id_num not in id_nums:
                id_nums.append(id_num)
                logging.debug(f"https://mall.industry.siemens.com/mall/en/ru/Catalog/Products/{id_num}?tree=CatalogTree")
    # исключение срабатывает если ветка развернута полностью, результат записывается в виде ссылки в отдельный файл для
    # каждой итерации и цикл продолжается до конца списка id_nums
    except Exception as e:
        logging.error(f"Error while processing ID {id_num}: {e}")
        product_pages.append(f"https://mall.industry.siemens.com/mall/en/ru/Catalog/Products/{id_num}?tree=CatalogTree")
        pass


def wait_for_element(driver, selector, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )


def get_products(x):
    driver.get(x)
    time.sleep(randrange(1, 3))
    ActionChains(driver)
    wait = WebDriverWait(driver, 10)
    while True:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "centerRegion")))
        driver.find_element(By.CSS_SELECTOR, "[class='pager nextPage']")
        if driver.find_element(By.CSS_SELECTOR, "[class='pager nextPage']").tag_name == 'a':
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "internalLinkMultiLines")))
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(randrange(1, 3))
            for href in driver.find_elements(By.CLASS_NAME, "internalLinkMultiLines"):
                url = href.get_attribute('href')
                if url not in urls:
                    with open('products_list1.txt', 'a') as txt_file:
                        txt_file.write("%s,\n" % url)
                    urls.append(url)
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(randrange(1, 3))
            driver.find_element(By.CSS_SELECTOR, "[class='pager nextPage']").click()
        elif driver.find_element(By.CSS_SELECTOR, "[class='pager nextPage']").tag_name == 'span':
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "internalLinkMultiLines")))
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(randrange(1, 3))
            for href in driver.find_elements(By.CLASS_NAME, "internalLinkMultiLines"):
                url = href.get_attribute('href')
                if url not in urls:
                    with open('products_list1.txt', 'a') as txt_file:
                        txt_file.write("%s,\n" % url)
                    urls.append(url)
            break


for page in product_pages:
    get_products(page)


workbook = openpyxl.Workbook()
worksheet = workbook.active
row = 2
n = 2
# добавляем колонки в таблицу
worksheet['A1'] = 'id'
worksheet['B1'] = 'parent_category'
worksheet['C1'] = 'child_category'
worksheet['D1'] = 'title'
worksheet['E1'] = 'unique_number'
worksheet['F1'] = 'info'
worksheet['G1'] = 'link_production'
# конвертируем собранные ссылки в список (сюда можно загрузить резервный список продуктов и запустить код с этого места)
with open("products_list1.txt", "r") as file:
    products = file.readlines()
products = [line.strip().rstrip(',') for line in products]

id = 1
# итерируем получившийся список
for product in products:
    s = requests.Session()
    response = s.get(url=product, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    # достаем нужную информацию из элементов
    article = soup.find('span', class_='productIdentifier').text
    category = soup.find('a', class_='internalLinkMultiLines').text
    description = soup.find('div', class_='productdescription').text
    title = soup.find('span', class_='productIdentifier').text
    items = soup.find('div', class_='Breadcrumb').find_all('div', class_='Item')
    # поиск родительской категории
    for item in items:
        parent_category = item.find('a', class_='breadcumbInternalLink')
        print(parent_category)
        if parent_category.text == 'Drive technology' or parent_category.text == 'Automation technology' or parent_category.text == 'Energy' or parent_category.text == 'Building Technologies' or parent_category.text == 'Safety Systems - Safety Integrated' or parent_category.text == 'Market-specific solutions' or parent_category.text == 'Digital Enterprise Services' or parent_category.text == '... and everything else you need':
            pc = parent_category.text
            print(pc)
            worksheet['B' + str(row)] = pc
    # записываем данные в Excel файл
    worksheet['A' + str(row)] = id
    worksheet['C' + str(row)] = category
    worksheet['D' + str(row)] = title
    worksheet['E' + str(row)] = article
    worksheet['F' + str(row)] = description
    worksheet['G' + str(row)] = product

    row += 1
    id += 1
    # saving table
    workbook.save('products123test.xlsx')
# занесем данные в базу данных
# для этого необходимо конвертировать таблицу в csv
data = pd.read_excel("название таблицы")
data.to_csv('file.csv', index=False)
# Вместо '#' нужно ввести данные своей Бд пароль, порт, название бд.
engine = create_engine('postgresql://postgres:####@###.##.###.#:###/###')

data.to_sql('product', engine, if_exists='append', index=False)