from bs4 import BeautifulSoup
import requests
import pandas as pd
from scraper import Scraper
import dateparser
import utils


class Bing(Scraper):
    def __init__(self):
        pass

    """
        scrapes data from bing

        Args:
            company_name (str): name of the company
            keyword (str): extra word to be searched along with the company name
            page_count (int): number of pages to be searched

        Returns:
            pd.DataFrame: will later be converted into csv
    """
    def scrape(self, company_name: str, keyword: str, page_count: int, base_url:str) -> pd.DataFrame:
        
        search_string = company_name + "+" + keyword
        all_news = []

        # pagination
        for i in range(page_count):
            url = f'{base_url}news/infinitescrollajax?qs=n&form=QBNT&sp=-1&lq=0&pq=te&sc=10-2&sk=&cvid=1590B94F6A1A40E89C0451EE4930A31D&ghsh=0&ghacc=0&ghpl=&InfiniteScroll=1&q={search_string}&first={i}1&IG=0E2CB393962B4A62A88816B1959CC59C&IID=news.5199&SFX={i}&PCW=1116'
            response = requests.get(url)

            timestamp = []
            if response.status_code == 200:

                soup = BeautifulSoup(response.content, "html.parser")
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
                        # fetching timestamp
                        for ele in soup.findChildren('span'):
                            if str(ele.get('aria-label')).endswith('ago'):
                                timestamp.append(ele.get('aria-label'))
                        news['timestamp'] = utils.format_timestamp(str(timestamp[count]))
                        count += 1
                    except Exception as e:
                        utils.log_message('Error in Bing: ' + str(e.args) + '\n')
                    news['search_engine'] = 'Bing'
                    news['search_string'] = company_name + " and " + keyword

                    all_news.append(news)

        return pd.DataFrame(all_news)
