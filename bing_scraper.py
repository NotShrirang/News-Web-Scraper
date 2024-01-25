import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
from scraper import Scraper


class Bing(Scraper):
    def __init__(self):
        pass

    def scrape(self, company_name: str, keyword: str, page_count: int) -> pd.DataFrame:
        search_string = company_name + keyword
        all_news = []

        for i in range(page_count):
            url = f'https://www.bing.com/news/infinitescrollajax?qs=n&form=QBNT&sp=-1&lq=0&pq=te&sc=10-2&sk=&cvid=1590B94F6A1A40E89C0451EE4930A31D&ghsh=0&ghacc=0&ghpl=&InfiniteScroll=1&q={search_string}&first={i}1&IG=0E2CB393962B4A62A88816B1959CC59C&IID=news.5199&SFX={i}&PCW=1116'
            response = requests.get(url)

            if response.status_code == 200:

                soup = BeautifulSoup(response.content, "html.parser")

                for anchor in soup:
                    if anchor is None:
                        continue
                    news = {}

                    news['link'] = anchor["data-url"]
                    news['title'] = anchor["data-title"]
                    news['source'] = anchor["data-author"]
                    try:
                        timestamp = str(anchor)[re.search(r"ago", str(
                            anchor)).start()-10: re.search(r"ago", str(anchor)).end()]
                        news['timestamp'] = timestamp[timestamp.find("\"")+1:]
                    except Exception as e:
                        with open('scraper.log', 'a') as f:
                            f.write('Error in Bing: ' +
                                    str(e.args) + '\n')
                    news['search_engine'] = 'bing'
                    news['search_string'] = company_name + " and " + keyword

                    all_news.append(news)

        return pd.DataFrame(all_news)
