import requests
from bs4 import BeautifulSoup
from scraper import Scraper
import pandas as pd


class Yahoo(Scraper):
    def __init__(self):
        pass

    def scrape(self, company_name: str, keyword: str, page_count: int) -> pd.DataFrame:
        BASE_URL = 'https://news.search.yahoo.com/search?q='

        response = requests.get(BASE_URL+company_name+'+'+keyword)
        soup = BeautifulSoup(response.text, 'lxml')

        NUMBER_OF_PAGES = page_count

        store = []

        for i in range(NUMBER_OF_PAGES):
            nws = {}
            all_news = soup.find_all('ul', class_='compArticleList')
            for news in all_news:
                # print(news)
                nws['Title'] = news.find('h4').text
                nws['Link'] = news.find('a')['href']
                nws['MediaAgency'] = news.find('span', class_='s-source mr-5 cite-co').text
                nws['Time'] = news.find('span', class_='fc-2nd s-time mr-8').text
                # print(news.find('h4').text)
                # print(news.find('a')['href'])
                # print(news.find('span', class_='s-source mr-5 cite-co').text)
                # print(news.find('span', class_='fc-2nd s-time mr-8').text)
                # print()
                store.append(nws)
                # print(store)
            url = soup.find('a', class_='next')['href']
            response = requests.get(url)
            print(url)
            soup = BeautifulSoup(response.content, 'lxml')

            return pd.DataFrame(store)


