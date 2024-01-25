from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import logging
import dateparser



logging.basicConfig(filename='logs.log',filemode="w",format="%(name)s -> %(levelname)s: %(message)s)")

def GoogleScraper(company,keywords,nop):
    titles=[]
    times=[]
    medias=[]
    links=[]
    j=1
    search_string=company+keywords
    try:
        while(j<=nop):
                response=requests.get(f"https://www.google.com/search?q={search_string}&tbm=nws&page={j}/")
                soup=bs(response.text,'html.parser')
                for title in soup.find_all('div',class_='Gx5Zad fP1Qef xpd EtOod pkphOe'):
                        titles.append(title.h3.text)
                        for p in title.find_all('div',class_="BNeawe UPmit AP7Wnd lRVwie"):
                            medias.append(p.text)
                        links.append(title.a['href'])
                        for p in title.find_all('span',class_="r0bn4c rQMQod"):
                            times.append(str(p.text))
                j+=1
        logging.info("scraping Done successfully!")
    except Exception as e:
        print("Error : ",e)
        logging.info("Error :"+str(e))
    for time in times:
        past=dateparser.parse(time)
        
    data={"Link":links,"Title":titles,"Source":medias,"Time":past,"Search Engine" :'google',"search String":search_string}
    df=pd.DataFrame(data)
    return df


