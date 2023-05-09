import json
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://www.russiadiscovery.ru/tours/page/"

browser = webdriver.Chrome()

# получаем каждую ссылку объявления c сайте
def take_all_links():
    data = {}
    for page in range(1, 2):
        url = f"{URL}{page}"
        browser.get(url)
        blocks = browser.find_element(By.CLASS_NAME, "tourListUl").find_elements(By.TAG_NAME, "li")
        for block in blocks:
            title = block.find_element(By.CLASS_NAME, 'tourList__title').text
            link = block.find_element(By.CLASS_NAME, "tourList__title").find_element(By.TAG_NAME, 'a').get_attribute('href')
            price = block.find_element(By.CLASS_NAME, 'tourList__price').text
            data[title] = {'title': title, "url": link, 'price': price}
    return data

# парсим данные с каждого блока
def extract_all_data(data):
    for post_url in data.values():
        browser.get(post_url['url'])
        try:
            group_zise = browser.find_elements(By.CLASS_NAME, 'tourPage__main__sidebar')[1].find_element(By.CLASS_NAME, 'tourPage__regions').text
            post_url['Что ожидает'] = group_zise
        except:
            print('Объект group_zise не найден')
            post_url['Что ожидает'] = 'не найден'

        photo_count = browser.find_element(By.CLASS_NAME, 'moreMediaGallery').text
        photo_count = int(photo_count.replace("+", '').replace(" ", '')) + 5
        post_url['photos'] = []

        for photo_num in range(1, photo_count):
            photo_url = f'{post_url["url"]}#&gid=1&pid={photo_num}'
            post_url['photos'].append(photo_url)

        with open('result2.json', "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)