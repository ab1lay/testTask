
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

url = 'https://www.goszakup.gov.kz/ru/registry/rqc'
visited = dict()

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(service=Service('geckodriver.exe'), options=options)    

driver.get(url)
time.sleep(2.5)
driver.execute_script("""
    let l = document.getElementsByTagName("rc-widget")[0];
    l.parentNode.removeChild(l);
""")
Select(driver.find_element(By.XPATH, '/html/body/main/div[4]/div[2]/div[3]/div[3]/div[4]/div/div[3]/div/div/select')).select_by_value('2000')
time.sleep(23)

def get_links(content):
    soup = bs(content, 'html.parser')
    links = soup.findAll('a', style='font-size: 13px')
    return [link.get('href') for link in links]

def get_row(link, driver):
    row = dict()
    driver.get(link)
    time.sleep(1)
    soup = bs(driver.page_source, 'html.parser')
    trs = soup.findAll('tr')
    for tr in trs:
        th = tr.find('th')
        td = tr.findAll('td')
        if len(td) > 1:
            row['Полный адрес организации'] = td[2].text
        elif th.text == 'Наименование на рус. языке':
            row['Наименование организации'] = td[0].text
        elif th.text == 'БИН участника':
            row['БИН организации'] = td[0].text
        elif th.text == 'ФИО':
            row['ФИО руководителя'] = td[0].text
        elif th.text == 'ИИН':
            row['ИИН руководителя'] = td[0].text
    return row 
        

links = get_links(driver.page_source)
result = []

for link in links:
    row = get_row(link, driver)
    name = row['Наименование организации']
    if not visited.get(name, False):
        result.append(row)
        visited[name] = True

driver.close()
driver.quit()

result = pd.DataFrame(result)
result.to_csv('result.csv', index_label='id')