import time
import random
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from fake_useragent import UserAgent

import requests

ID = ''
API_TOKEN = ''

def get_active_days():
    useragent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={useragent.random}")
    options.add_argument("--headless")

    driver = webdriver.Chrome('./chromedriver/chromedriver', options=options)
    try:
        driver.get(url="https://programarecetatenie.eu/")
        #test webarhiv
        # driver.get(url="https://web.archive.org/web/20230329122940/https://programarecetatenie.eu/")
        type_program = driver.find_element(by=By.ID, value='select2-tip_formular-container')
        type_program.click()
        program_types = driver.find_elements(by=By.CLASS_NAME, value='select2-results__option')
        program_types[1].click()
        driver.execute_script("window.scrollBy(0,1000)", "")
        time.sleep(0.25)
        find_active = driver.find_elements(by=By.CSS_SELECTOR, value='.day:not([class*=" "])')
        while driver.find_elements(by=By.CSS_SELECTOR, value='.next:not([class*=" "])'):
            next_aa = driver.find_elements(by=By.CLASS_NAME, value="next")
            next_aa[0].click()
            find_active += driver.find_elements(by=By.CSS_SELECTOR, value='.day:not([class*=" "])')
        return find_active

    except:
        # driver.save_screenshot('screen.png')
        # # send_photo('screen.png')
        # os.remove('screen.png')
        print("smt wrong")

    finally:
        driver.close()
        driver.quit()


def send_message(msg):
    api_url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"
    payload = {
        'chat_id': ID,
        'text': msg
    }
    requests.post(api_url, json=payload)


def send_photo(photo_path, caption=None):
    api_url = f"https://api.telegram.org/bot{API_TOKEN}/sendPhoto"
    payload = {
        'chat_id': ID,
        'caption': caption
    }
    files = {
        'photo': open(photo_path, 'rb')
    }
    response = requests.post(api_url, data=payload, files=files)

def main():
    while True:
        if get_active_days():
            send_message("We have smt for you")
        time.sleep(60)

if __name__ == '__main__':
    main()

