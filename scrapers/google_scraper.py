import bs4
import requests
import pandas as pd
from .scraper import Scraper
from utils import logger, date_utils
import dateparser



class Google(Scraper):
    def __init__(self):
        pass

    """
        scrapes data from google

        Args:
            company_name (str): name of the company
            keyword (str): extra word to be searched along with the company name
            page_count (int): number of pages to be searched

        Returns:
            pd.DataFrame: will later be converted into csv
    """

    # def scrape(self, company_name: str, keyword: str, page_count: int, base_url: str) -> pd.DataFrame:
    #     all_news = []
    #     NUMBER_PAGE = page_count
    #     query = company_name + " " + keyword
    #     next_link = "*****"

    #     # pagination
    #     for i in range(NUMBER_PAGE):
    #         if next_link == "*****":
    #             response = requests.get(
    #                 base_url+"search?q={" + query + "}&tbm=nws")
    #             soup = bs4.BeautifulSoup(response.content, features="lxml")
    #             next_link = [element for element in soup.find_all(
    #                 'a') if element.get('aria-label') == 'Next page'][0].get('href')
    #         else:
    #             response = requests.get(base_url+next_link)
    #             soup = bs4.BeautifulSoup(response.content, features="lxml")
    #             try:
    #                 next_link = [element for element in soup.find_all(
    #                     'a') if element.get('aria-label') == 'Next page'][0].get('href')
    #             except Exception as e:
    #                 logger.log_message(
    #                     'Error in Google: ' + str(e.args) + '\n')
    #                 break
    #         for element in soup.select("div>a"):
    #             if str(element.text).endswith('ago'):
    #                 news = {}
    #                 news['link'] = str(element.get(
    #                     'href')).replace("/url?q=", "")
    #                 news['title'] = element.select('h3>div')[0].text
    #                 for child in element.children:
    #                     ele = child.select("div>div")
    #                     if len(ele) == 4:
    #                         news['source'] = child.select("div>div")[3].text
    #                         news['timestamp'] = date_utils.format_timestamp(
    #                             element.select('span')[0].text)
    #                         break
    #                     else:
    #                         if len(ele[0].select('span')) == 5:
    #                             news['source'] = ele[0].select('span')[3].text
    #                             news['timestamp'] = ele[0].select('span')[
    #                                 4].text
    #                 news['search_engine'] = 'google'
    #                 news['page_count'] = i+1
    #                 news['search_string'] = company_name + " and " + keyword
    #                 all_news.append(news)

    #     final_df = pd.DataFrame(all_news)
    #     return final_df

    def scrape(self, company_name: str, keyword: str, page_count: int, base_url: str):
        '''
        This method scrapes data based on the given search string from Google search engine

        Parameters:
            company    : Company name.
            keywords   : List of keywords.
            page_count : Number of pages to scrap.
            
        Returns:
            df : DataFrame of scraped data from Google search engine.
            
        '''
        titles=[]
        times=[]
        medias=[]
        links=[]
        j=1
        query = company_name + " " + keyword
        # search_string=company+" "+keywords
        try:
            while(j<=page_count):
                    response = requests.get(base_url+"search?q={" + query + "}&tbm=nws")
                    # response=requests.get(f"https://www.google.com/search?q={search_string}&tbm=nws&page={j}/")
                    soup=bs4(response.text,'html.parser')
                    for title in soup.find_all('div',class_='Gx5Zad fP1Qef xpd EtOod pkphOe'):
                            titles.append(title.h3.text)
                            for p in title.find_all('div',class_="BNeawe UPmit AP7Wnd lRVwie"):
                                medias.append(p.text)
                            links.append((title.a['href']).replace("/url?q=",""))
                            for p in title.find_all('span',class_="r0bn4c rQMQod"):
                                times.append(dateparser.parse(str(p.text)))
                    j+=1
            
        except Exception as e:
    #         logger.log_message(
    # #                     'Error in Google: ' + str(e.args) + '\n')
            logger.log_message(f'An error occured: {e}', level=1)
            # logging.error(f'An error occured: {e}',exec_info=True)
        #     ,link,title,source,timestamp,search_engine,page_count,search_string
        # data={"link":links,"title":titles,"source":medias,"timestamp":times,"search_engine" :'google',"search String":query}

        data = {"title": titles, "link": links, "source": medias,
                "timestamp": times, 'search_engine': 'google', 'page_number': j, 'search_string': query}
        df=pd.DataFrame(data)
        return df