import bs4
import requests
import pprint
import pandas as pd

BASE_URL = 'https://www.google.com/'


def scrape(query: str, page_count: int):
    all_news = []
    NUMBER_PAGE = page_count
    next_link = "*****"
    for i in range(NUMBER_PAGE):
        if next_link == "*****":
            response = requests.get(
                BASE_URL+"search?q={" + query + "}&tbm=nws")
            soup = bs4.BeautifulSoup(response.content, features="lxml")
            next_link = [element for element in soup.find_all(
                'a') if 'Next' in str(element.text)][0].get('href')
            print(next_link)
        else:
            response = requests.get(BASE_URL+next_link)
            soup = bs4.BeautifulSoup(response.content, features="lxml")
            next_link = [element for element in soup.find_all(
                'a') if element.get('aria-label') == 'Next page'][0].get('href')
            print(next_link)
        for element in soup.select("div>a"):
            if str(element.text).endswith('ago'):
                news = {}
                news['link'] = element.get('href')
                news['title'] = element.select('h3>div')[0].text
                print(element.get('href'), element.select('h3>div')[0].text)
                for child in element.children:
                    ele = child.select("div>div")
                    if len(ele) == 4:
                        news['source'] = child.select("div>div")[3].text
                        news['timestamp'] = element.select('span')[0].text
                        pprint.pprint(child.select("div>div")[3].text)
                        pprint.pprint(element.select('span')[0].text)
                        break
                    else:
                        if len(ele[0].select('span')) == 5:
                            news['source'] = ele[0].select('span')[3].text
                            news['timestamp'] = ele[0].select('span')[4].text
                            pprint.pprint(ele[0].select('span')[3].text)
                            pprint.pprint(ele[0].select('span')[4].text)
                all_news.append(news)

    final_df = pd.DataFrame(all_news)
    return final_df
