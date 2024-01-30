# import necessary libraries
import bs4
import requests
import pandas as pd
from .scraper import Scraper
from utils import logger, date_utils
import dateparser



class Google(Scraper):
    def __init__(self):
        pass

    def scrape(self, company_name: str, keyword: str, page_count: int, base_url: str):
        """
        This method scrapes data based on the given search string from Google search engine

        Args:
            company_name (str): name of the company
            keyword (str): extra word to be searched along with the company name
            page_count (int): number of pages to be searched
            base_url (str): base URL for constructing search requests
                
        Returns:
            df : DataFrame of scraped data from Google search engine.
            
        """
        titles=[]
        times=[]
        medias=[]
        links=[]
        j=1
        query = company_name + " " + keyword
        # search_string=company+" "+keywords
        try:
            while(j<=page_count):
                    # https://www.google.com/search?q={query}&tbm=nws&page={j}/
                    # response = requests.get(base_url+f"search?q={query}&tbm=nws&page={j}/")
                    response = requests.get(f"https://www.google.com/search?q={query}&tbm=nws&page={j}/")
                    # response=requests.get(f"https://www.google.com/search?q={query}&tbm=nws&page={j}/")
                    soup=bs4.BeautifulSoup(response.text,'html.parser')
                    for title in soup.find_all('div',class_='Gx5Zad fP1Qef xpd EtOod pkphOe'):
                            titles.append(title.h3.text)
                            for p in title.find_all('div',class_="BNeawe UPmit AP7Wnd lRVwie"):
                                medias.append(p.text)
                            links.append((title.a['href']).replace("/url?q=",""))
                            for p in title.find_all('span',class_="r0bn4c rQMQod"):
                                times.append(dateparser.parse(str(p.text)))
                    j+=1
            
        except Exception as e:

            logger.log_message(f'An error occured: {e}', level=1)


        data = {"title": titles, "link": links, "source": medias,
                "timestamp": times, 'search_engine': 'google', 'page_count': j, 'search_string': query}
        df=pd.DataFrame(data)
        return df
