import time
from random import randrange
import openpyxl
from sqlalchemy import create_engine
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup


#инициализируем списки различных собираемых данных

id_nums = []
id_names = ["hyperlinkDrivetechnology", "hyperlinkAutomationtechnology", "hyperlinkEnergy", "hyperlinkBuildingTechnologies", "hyperlinkSafetySystems-SafetyIntegrated", "hyperlinkMarket-specificsolutions", "hyperlinkDigitalEnterpriseServices"]
urls = []
# #подготавливаем заголовки для отправки запросов
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0 (Edition Yx GX)"
}
# #посылаем запрос на стартовую страницу и собираем ссылки родительских категорий
s = requests.Session()
response = s.get(url="https://mall.industry.siemens.com/mall/en/ru/Catalog/Products/1000000", headers=headers)
soup = BeautifulSoup(response.text, "lxml")
for name in id_names:
    title_url = soup.find('a', id =f'{name}')
    urls.append(title_url.get('href'))
# # инициализируем списки для итерации ссылок всех категорий древа
item_links = []
n = 1
product_pages = []
# # запускаем цикл итерации всех родительских ссылок для получения первой развертки древа категорий
for url in urls:
    # из ссылок полученных ранее достаем айди страницы, чтобы можно было находить конкретные элементы на странице
    id_num = url.split('/')[-1]
    s = requests.Session()
    response = s.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    # находим нужные элементы
    branch = soup.find('a', id=f"{id_num}").find_next('div', class_="PopupItems").find_all('a', class_="internalLink")
    # итерируем найденные элементы и пополняем изначальный список значениями которых там еще нет
    for item in branch:
        id_num = item.get('href').split("/")[-1]
        if id_num not in id_nums:
            id_nums.append(id_num)
print(len(id_nums))
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
                print(f"https://mall.industry.siemens.com/mall/en/ru/Catalog/Products/{id_num}?tree=CatalogTree")
    # исключение срабатывает если ветка развернута полностью, результат записывается в виде ссылки в отдельный файл для
    # каждой итерации и цикл продолжается до конца списка id_nums
    except:
        with open('резервный список продуктов 06-02-2023.txt', 'a') as txt_file:
            txt_file.write("%s,\n" % f"https://mall.industry.siemens.com/mall/en/ru/Catalog/Products/{id_num}?tree=CatalogTree")
        pass
        print("конечная страница "+f"https://mall.industry.siemens.com/mall/en/ru/Catalog/Products/{id_num}?tree=CatalogTree")
print(len(id_nums))

executable_path = "C:/chromedriver.exe"
service = ChromeService(executable_path=executable_path)
driver = webdriver.Chrome(service=service)
workbook = openpyxl.Workbook()
worksheet = workbook.active
# adding columns
worksheet['A1'] = 'id'
worksheet['B1'] = 'parent_category'
worksheet['C1'] = 'child_category'
worksheet['D1'] = 'title'
worksheet['E1'] = 'unique_number'
worksheet['F1'] = 'info'
worksheet['G1'] = 'link_production'
with open("products_list1.txt", "r") as file:
    products = file.readlines()
products = [line.strip().rstrip(',') for line in products]
with open("резервный список продуктов 06-02-2023.txt", "r") as file:
    lines = file.readlines()
lines = [line.strip().rstrip(',') for line in lines]

urls = []

row = 2
n = 2


def get_products(x):
    driver.get(x)
    time.sleep(randrange(1,3))
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)
    while True:
        next_page = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "centerRegion")))
        span = driver.find_element(By.CSS_SELECTOR, "[class='pager nextPage']")
        if driver.find_element(By.CSS_SELECTOR, "[class='pager nextPage']").tag_name == 'a':
            items = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "internalLinkMultiLines")))
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
            print('naideno neskolko str: ', len(urls))
        elif driver.find_element(By.CSS_SELECTOR, "[class='pager nextPage']").tag_name == 'span':
            items = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "internalLinkMultiLines")))
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(randrange(1, 3))
            for href in driver.find_elements(By.CLASS_NAME, "internalLinkMultiLines"):
                url = href.get_attribute('href')
                if url not in urls:
                    with open('products_list1.txt', 'a') as txt_file:
                        txt_file.write("%s,\n" % url)
                    urls.append(url)

            print('naidena odna str: ', len(urls))

            break


for line in lines:
    if len(urls) < 54:
        get_products(line)
row = 2
id = 1
for product in products:
    print(id)
    s = requests.Session()
    response = s.get(url=product, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    article = soup.find('span', class_='productIdentifier').text
    category = soup.find('a', class_='internalLinkMultiLines').text
    description = soup.find('div', class_='productdescription').text
    title = soup.find('span', class_='productIdentifier').text
    # hidden = soup.find_element(By.ID, "ellipseItem")
    # hidden.click()
    items = soup.find('div', class_='Breadcrumb').find_all('div', class_='Item')
    for item in items:
        parent_category = item.find('a', class_='breadcumbInternalLink')
        print(parent_category)
        if parent_category.text == 'Drive technology' or parent_category.text == 'Automation technology' or parent_category.text == 'Energy' or parent_category.text == 'Building Technologies' or parent_category.text == 'Safety Systems - Safety Integrated' or parent_category.text == 'Market-specific solutions' or parent_category.text == 'Digital Enterprise Services' or parent_category.text == '... and everything else you need':
            pc = parent_category.text
            print(pc)
            worksheet['B' + str(row)] = pc
    worksheet['A' + str(row)] = id
    worksheet['C' + str(row)] = category
    worksheet['D' + str(row)] = title
    worksheet['E' + str(row)] = article
    worksheet['F' + str(row)] = description
    worksheet['G' + str(row)] = product

    row += 1
    id += 1
    # saving table
    workbook.save('products123.xlsx')










