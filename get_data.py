import requests
from bs4 import BeautifulSoup
import csv
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


def str_to_digit(string):
    if string == "توافقی" or string == "برای معاوضه" or string == "غیرقابل نمایش":
        return "توافقی"
    result = "".join(re.findall(r'\d+', string.replace(',', '')))
    return str(int(result))


def get_car_data(user_car, user_car_year, mode):
    try:
        with open(file=f"./cars_data/{user_car.replace('/','_')}.csv", mode=mode, encoding='utf-8', newline="\n") as cf:
            writer = csv.writer(cf)
            writer.writerow(['year', 'usage', 'price'])
    except:
        print('done')
        return

    url = f"https://divar.ir/s/tehran/car/{user_car}?production-year={int(user_car_year)+1}-{int(user_car_year)-1}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'}
    # response = requests.get(
    #     f"https://divar.ir/s/tehran/car/{user_car}?production-year={int(user_car_year)+1}-{int(user_car_year)-1}", headers=headers)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(5)
    scroll_pause_time = 3
    screen_height = driver.execute_script('return window.screen.height;')
    cars_cards = []
    for i in range(30):
        # scroll one screen height each time
        driver.execute_script(
            "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script(
            "return document.body.scrollHeight;")

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        cards = soup.find_all(
            'div', {'class': "waf972"})
        for card in cards:
            if card not in cars_cards:
                cars_cards.extend(card)

        if (screen_height) * i > scroll_height:
            break

    print('catching data')
    for car in cars_cards:
        sub_url = 'https://divar.ir'+car.find('a')['href']
        sub_res = requests.get(sub_url, headers=headers)
        sub_soup = BeautifulSoup(sub_res.text, 'html.parser')
        cars_detail = sub_soup.find_all(
            'span', {'class': 'kt-group-row-item__value'})
        year = int(cars_detail[1].text)
        usage = str_to_digit(cars_detail[0].text)
        price = sub_soup.find_all(
            'p', {'class': 'kt-unexpandable-row__value'})
        price = str_to_digit(price[len(price)-1].text)
        with open(file=f"./cars_data/{user_car.replace('/','_')}.csv", mode='a', encoding='utf-8', newline="\n") as cf:
            writer = csv.writer(cf)
            if price != "توافقی":
                writer.writerow([year, usage, price])
    print('updated')
