# import necessary libraries
import bs4
import requests
import pandas as pd
from .scraper import Scraper
from utils import logger, date_utils


class Google(Scraper):
    def __init__(self):
        pass

    def scrape(self, company_name: str, keyword: str, page_count: int, base_url: str) -> pd.DataFrame:
        """
        scrapes data from google

        Args:
            company_name (str): name of the company
            keyword (str): extra word to be searched along with the company name
            page_count (int): number of pages to be searched
            base_url (str): base URL for constructing search requests.

        Returns:
            pd.DataFrame: will later be converted into csv
    """
        all_news = []
        NUMBER_PAGE = page_count
        query = company_name + " " + keyword
        next_link = "*****"  # placeholder for initial value

        # pagination
        for i in range(NUMBER_PAGE):
            if next_link == "*****":
                # first page request
                response = requests.get(
                    base_url+"search?q={" + query + "}&tbm=nws")
                soup = bs4.BeautifulSoup(response.content, features="lxml")
                # Extract link for the next page
                next_link = [element for element in soup.find_all(
                    'a') if element.get('aria-label') == 'Next page'][0].get('href')
            else:
                # Subsequent page requests
                response = requests.get(base_url+next_link)
                soup = bs4.BeautifulSoup(response.content, features="lxml")
                try:
                    # Gets the link for the next page
                    next_link = [element for element in soup.find_all(
                        'a') if element.get('aria-label') == 'Next page'][0].get('href')
                except Exception as e:
                    logger.log_message(
                        'Error in Google: ' + str(e.args) + '\n')
                    break

            # Extract news data from the current page
            for element in soup.select("div>a"):
                if str(element.text).endswith('ago'):
                    news = {}
                    # Extracting link, title, source, and timestamp
                    news['link'] = str(element.get(
                        'href')).replace("/url?q=", "")
                    news['title'] = element.select('h3>div')[0].text
                    for child in element.children:
                        ele = child.select("div>div")
                        if len(ele) == 4:
                            news['source'] = child.select("div>div")[3].text
                            news['timestamp'] = date_utils.format_timestamp(
                                element.select('span')[0].text)
                            break
                        else:
                            if len(ele[0].select('span')) == 5:
                                news['source'] = ele[0].select('span')[3].text
                                news['timestamp'] = ele[0].select('span')[
                                    4].text
                    # Adding additional information to the news
                    news['search_engine'] = 'google'
                    news['page_count'] = i+1
                    news['search_string'] = company_name + " and " + keyword
                    # Adding news dictionary to list
                    all_news.append(news)

        # Creating final Data Frame
        final_df = pd.DataFrame(all_news)
        return final_df
