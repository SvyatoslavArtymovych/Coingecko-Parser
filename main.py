import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from config import *
from excel_funks import *
from telegram_bot import *

chrome_options = Options()


browser = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
wait = WebDriverWait(browser, 60)


def load_pages():
    try:
        print('Try to load more')
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='btn btn-primary btn-sm mt-3' and @style='']")))
        browser.find_element_by_xpath("//a[@class='btn btn-primary btn-sm mt-3' and @style='']").click()
    except:
        print('Loading ended')


def translate_date(date):
    month = str(date).split()[0]
    day = str(date).split()[1]
    year = str(date).split()[2]
    return f'{year}-{MONTH[month]}-{day[:2]}'


def parser():
    write_empty_row()

    while True:
        try:
            print('Try to load more')
            wait.until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='btn btn-primary btn-sm mt-3' and @style='']")))
            browser.find_element_by_xpath("//a[@class='btn btn-primary btn-sm mt-3' and @style='']").click()
        except:
            print('Loading ended')
            break

    table = browser.find_element_by_xpath("//table[@id='gecko-table-all']//tbody[@data-target='all-coins.tablebody']")
    index = table.find_elements_by_xpath("//td[@class='table-number']")
    coins = table.find_elements_by_xpath("//div[@class='d-flex']//a[@href]")
    for i in range(start_position, len(index)):
        URL = coins[i].get_attribute('href')
        HEADERS = {'user_agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)  Chrome/86.0.4240.183 Safari/537.36'}

        page = requests.get(URL, headers=HEADERS)
        tree = html.fromstring(page.content)

        e = tree.xpath("//tr/th[text()='All-Time Low']//following::td/span[@class='no-wrap']/following::small")
        try:
            if translate_date(str(e[0].text)) == find_date:
                write_information([index[i].text,
                                   str(coins[i].get_attribute('href')).split('/')[-1].title(),
                                   translate_date(str(e[0].text)),
                                   URL])
                send_message(index[i].text,
                             str(coins[i].get_attribute('href')).split('/')[-1].title(),
                             translate_date(str(e[0].text)),
                             URL)
        except IndexError:
            pass

        try:
            print(f"{index[i].text} | "
                  f"{str(coins[i].get_attribute('href')).split('/')[-1].title()} | "
                  f"{translate_date(str(e[0].text))}")
        except IndexError:
            print('Error')

    print(f'Pause {restart_by_mins/60} min.')
    sleep(restart_by_mins)


if __name__ == "__main__":
    create_table()

    browser.get(site)

    while True:
        parser(site)
