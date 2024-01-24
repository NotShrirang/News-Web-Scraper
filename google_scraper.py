import bs4
import requests
import pandas as pd
from scraper import Scraper


class Google(Scraper):
    def __init__(self):
        self.BASE_URL = 'https://www.google.com/'
        pass

    def scrape(self, company_name: str, keyword: str, page_count: int) -> pd.DataFrame:
        """Scrapes the news from google.com

        Args:
            company_name (str): company name to search
            keyword (str): keyword to search
            page_count (int): number of pages to scrape

        Returns:
            pd.DataFrame: dataframe containing the scraped data
        """
        all_news = []
        NUMBER_PAGE = page_count
        query = company_name + " " + keyword
        next_link = "*****"
        for i in range(NUMBER_PAGE):
            if next_link == "*****":
                response = requests.get(
                    self.BASE_URL+"search?q={" + query + "}&tbm=nws")
                soup = bs4.BeautifulSoup(response.content, features="lxml")
                next_link = [element for element in soup.find_all(
                    'a') if 'Next' in str(element.text)][0].get('href')
            else:
                response = requests.get(self.BASE_URL+next_link)
                soup = bs4.BeautifulSoup(response.content, features="lxml")
                next_link = [element for element in soup.find_all(
                    'a') if element.get('aria-label') == 'Next page'][0].get('href')
            for element in soup.select("div>a"):
                if str(element.text).endswith('ago'):
                    news = {}
                    news['link'] = element.get('href')
                    news['title'] = element.select('h3>div')[0].text
                    for child in element.children:
                        ele = child.select("div>div")
                        if len(ele) == 4:
                            news['source'] = child.select("div>div")[3].text
                            news['timestamp'] = element.select('span')[0].text
                            break
                        else:
                            if len(ele[0].select('span')) == 5:
                                news['source'] = ele[0].select('span')[3].text
                                news['timestamp'] = ele[0].select('span')[
                                    4].text
                    news['search_engine'] = 'google'
                    news['page_count'] = page_count
                    news['search_string'] = company_name + " and " + keyword
                    all_news.append(news)

        final_df = pd.DataFrame(all_news)
        return final_df
