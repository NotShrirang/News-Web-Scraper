from bs4 import BeautifulSoup
import requests
import pandas as pd
from scraper import Scraper
import dateparser


class Bing(Scraper):
    def __init__(self):
        pass

    def scrape(self, company_name: str, keyword: str, page_count: int) -> pd.DataFrame:
        search_string = company_name + "+" + keyword
        all_news = []

        for i in range(page_count):
            url = f'https://www.bing.com/news/infinitescrollajax?qs=n&form=QBNT&sp=-1&lq=0&pq=te&sc=10-2&sk=&cvid=1590B94F6A1A40E89C0451EE4930A31D&ghsh=0&ghacc=0&ghpl=&InfiniteScroll=1&q={search_string}&first={i}1&IG=0E2CB393962B4A62A88816B1959CC59C&IID=news.5199&SFX={i}&PCW=1116'
            response = requests.get(url)

            timestamp = []
            if response.status_code == 200:

                soup = BeautifulSoup(response.content, "html.parser")
                count = 0
                for div in soup:
                    if div is None:
                        continue
                    news = {}

                    news['link'] = div["data-url"]
                    news['title'] = div["data-title"]
                    news['source'] = div["data-author"]
                    try:
                        for ele in soup.findChildren('span'):
                            if str(ele.get('aria-label')).endswith('ago'):
                                timestamp.append(ele.get('aria-label'))
                        news['timestamp'] = dateparser.parse(timestamp[count])
                        count += 1
                    except Exception as e:
                        with open('scraper.log', 'a') as f:
                            f.write('Error in Bing: ' +
                                    str(e.args) + '\n')
                    news['search_engine'] = 'Bing'
                    news['search_string'] = company_name + " and " + keyword

                    all_news.append(news)

        return pd.DataFrame(all_news)
