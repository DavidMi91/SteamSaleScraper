import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time

url = 'https://store.steampowered.com/search/results/?query&start=50&count=50&dynamic_data=&force_infinite=1&filter=topsellers&snr=1_7_7_7000_7&infinite=1'

def totalresults(url):
    r = requests.get(url)
    data = dict(r.json())
    totalresults = data['total_count']
    return int(totalresults)

def get_data(url):
    r = requests.get(url)
    data = dict(r.json())
    return data['results_html']

print(get_data(url))

def parse (data):
    gameslist = [];
    soup = BeautifulSoup(data, 'html.parser')
    games = soup.find_all('a')
    for game in games:
        title = game.find('span', {'class': 'title'}).text
        price = game.find('div', {'class': 'search_price'}).text.strip().split('€')[0]
        try:
            discprice = game.find('div', {'class': 'search_price'}).text.strip().split('€')[1]
        except:
            discprice = price
        print(title,price)

        mygame ={
            'title': title,
            'price': price,
            'discprice': discprice
        }
        gameslist.append(mygame)
    return gameslist

def output(gameslist):
    gamesdf = pd.concat([pd.DataFrame(g) for g in results])
    gamesdf.to_csv('gamesprices.csv', index=False)
    print('Fin. Saved to CSV')
    return

results = []
for x in range(0, 150, 50):
    data = get_data(f'https://store.steampowered.com/search/results/?query&start={x}&count=50&dynamic_data=&force_infinite=1&filter=topsellers&snr=1_7_7_7000_7&infinite=1')
    results.append(parse(data))
    print('Results scraped: ', x)
    time.sleep(1.5)

output(results)


