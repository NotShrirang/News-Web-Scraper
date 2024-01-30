#import necessary libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
from .scraper import Scraper
from utils import logger, date_utils


class Bing(Scraper):
    def __init__(self):
        pass

    def scrape(self, company_name: str, keyword: str, page_count: int, base_url: str) -> pd.DataFrame:
    """
        Scrapes data from Bing

        Args:
            company_name (str): name of the company
            keyword (str): extra word to be searched along with the company name
            page_count (int): number of pages to be searched
            base_url (str): Base URL for constructing search requests.

        Returns:
            pd.DataFrame: will later be converted into csv
    """
        search_string = company_name + "+" + keyword
        all_news = []

        # pagination
        for i in range(page_count):
            url = f'{base_url}news/infinitescrollajax?qs=n&form=QBNT&sp=-1&lq=0&pq=te&sc=10-2&sk=&cvid=1590B94F6A1A40E89C0451EE4930A31D&ghsh=0&ghacc=0&ghpl=&InfiniteScroll=1&q={search_string}&first={i}1&IG=0E2CB393962B4A62A88816B1959CC59C&IID=news.5199&SFX={i}&PCW=1116'
            response = requests.get(url)

            timestamp = []
            if response.status_code == 200:

                soup = BeautifulSoup(response.content, "html.parser")

                try:
                    # fetching timestamp
                    for ele in soup.findChildren('span'):
                        if str(ele.get('aria-label')).endswith('ago'):
                            timestamp.append(ele.get('aria-label'))
                except Exception as e:
                    logger.log_message(message='Error in Bing: ' + str(e.args),level=1)

                count = 0
                for div in soup:
                    if div is None:
                        continue
                    news = {}

                    # fetcing required data from attributes 
                    news['link'] = div["data-url"]
                    news['title'] = div["data-title"]
                    news['source'] = div["data-author"]
                    try:
                        news['timestamp'] = date_utils.format_timestamp(str(timestamp[count]))
                    except Exception as e:
                        logger.log_message(message='Error in Bing: ' + str(e.args), level=1)
                    count += 1
                    news['search_engine'] = 'Bing'
                    news['page_count'] = i + 1
                    news['search_string'] = company_name + " and " + keyword

                    all_news.append(news)

        return pd.DataFrame(all_news)
