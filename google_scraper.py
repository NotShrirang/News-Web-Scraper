import bs4
import requests
import pandas as pd
from scraper import Scraper
import dateparser


class Google(Scraper):
    def __init__(self):
        self.BASE_URL = 'https://www.google.com/'
        pass

    def scrape(self, company_name: str, keyword: str, page_count: int) -> pd.DataFrame:
        """scrapes data from google

        Args:
            company_name (str): name of the company
            keyword (str): extra word to be searched along with the company name
            page_count (int): number of pages to be searched

        Returns:
            pd.DataFrame: will later be converted into csv
        """
        all_news = []
        NUMBER_PAGE = page_count
        query = company_name + " " + keyword
        next_link = "*****"

        # pagination
        for i in range(NUMBER_PAGE):
            if next_link == "*****":
                response = requests.get(
                    self.BASE_URL+"search?q={" + query + "}&tbm=nws")
                soup = bs4.BeautifulSoup(response.content, features="lxml")
                next_link = [element for element in soup.find_all('a') if 'Next' in str(element.text)][0].get('href')
            else:
                response = requests.get(self.BASE_URL+next_link)
                soup = bs4.BeautifulSoup(response.content, features="lxml")
                next_link = [element for element in soup.find_all('a') if element.get('aria-label') == 'Next page'][0].get('href')
            for element in soup.select("div>a"):
                if str(element.text).endswith('ago'):
                    news = {}
                    news['link'] = str(element.get('href')).replace("/url?q=", "")
                    news['title'] = element.select('h3>div')[0].text
                    for child in element.children:
                        ele = child.select("div>div")
                        if len(ele) == 4:
                            news['source'] = child.select("div>div")[3].text
                            news['timestamp'] = dateparser.parse(element.select('span')[0].text)
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
