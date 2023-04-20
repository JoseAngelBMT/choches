import requests
from bs4 import BeautifulSoup
import time
import random
import datetime
import configparser

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0',
            'Accept-Language': 'es',
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8"}

config = configparser.ConfigParser()
config.read('config.ini')

x = datetime.datetime.now()

urls = ['https://www.coches.net/segunda-mano/?KeyWords=Performance&MakeId=18&ModelId=622&MaxPrice=30000&MaxKms=60000']

bot_token = config['credentials']['token']
chat_id = config['credentials']['id']

def send_telegram(img_src, message):
    if img_src:
        telegram_url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
        r = requests.post(telegram_url, data={'chat_id': chat_id}, files={'photo': requests.get(img_src).content})
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=payload)
    print(response.content)

def search_cars():
    results = []
    for url in urls:
        print(url)
        response = requests.get(url, headers = headers)

        soup = BeautifulSoup(response.content, 'html.parser')

        cars = soup.find_all('section', {'class': "mt-AdsList-content"})[:5]

        for car in cars:
            try:
                title = car.find('h2', {'class': "mt-CardBasic-title"}).text.strip()
                price = car.find('h3', {'class': "mt-TitleBasic-title mt-TitleBasic-title--s mt-TitleBasic-title--currentColor"}).text.strip()
                info = car.find('a', {'class': "mt-CardBasic-titleLink"})
                link = "coches.net"+ info['href']
                imgs = car.find('figure', {'class': "sui-AtomImage-figure"})
                img_tag = imgs.find('img')
                img_src = img_tag['src']    
                results.append({'portal': 'Choches.net', 'title': title, 'price': price, 'link': link, 'imgs':img_src})
            except:
                print(x, "Error parsing information")

    return results

interval = 3600

while True:
    results = search_cars()
    if results:
        message = f'A new car has been found:\n\n{results[0]["title"]} ({results[0]["price"]})\n\n{results[0]["link"]}'
        send_telegram(results[0]["imgs"], message)
    else:
        print(x, 'No results found.')

    interval = random.randint(3000, 4000)
    time.sleep(interval)
