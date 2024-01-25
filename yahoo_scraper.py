import requests
from bs4 import BeautifulSoup
from scraper import Scraper
import pandas as pd
import dateparser
import utils


class Yahoo(Scraper):
    def __init__(self):
        pass

    """
        scrapes data from yahoo

        Args:
            company_name (str): name of the company
            keyword (str): extra word to be searched along with the company name
            page_count (int): number of pages to be searched

        Returns:
            pd.DataFrame: 
    """
    def scrape(self, company_name: str, keyword: str, page_count: int, base_url:str) -> pd.DataFrame:
        url = base_url + 'search?q='

        response = requests.get(url+company_name+keyword)
        soup = BeautifulSoup(response.text, 'lxml')
        NUMBER_OF_PAGES = page_count

        titles, links, media, time, searchEngine, searchString = [], [], [], [], [], []

        # pagination
        for _ in range(NUMBER_OF_PAGES):
            all_news = soup.find_all('ul', class_='compArticleList')
            for news in all_news:
                titles.append(news.find('h4').text)
                links.append(news.find('a')['href'])
                media.append(
                    news.find('span', class_='s-source mr-5 cite-co').text)
                time.append(
                    news.find('span', class_='fc-2nd s-time mr-8').text.replace('.', ''))
                searchString.append(company_name+' and '+keyword)
                searchEngine.append('Yahoo')
            
            try:
                # gets data from next page 
                nextResponse = requests.get(
                    soup.find('a', class_='next')['href'])
                soup = BeautifulSoup(nextResponse.content, 'lxml')
            except Exception as e:
                utils.log_message('Error in Yahoo: ' + str(e.args) + '\n')
        
        # to get the actual date
        ParsedTime = []
        for t in time:
            ParsedTime.append(utils.format_timestamp(str(t)))
    
        data = {"title": titles, "link": links, "source": media,
                "timestamp": ParsedTime, 'search_engine': searchEngine, 'search_string': searchString}
        return pd.DataFrame(data)
