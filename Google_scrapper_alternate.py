from bs4 import BeautifulSoup as bs
import requests
import pandas as pd



def GoogleScrapper(company,keywords,nop):
    titles=[]
    times=[]
    medias=[]
    links=[]
    j=1
    search_string=company+keywords
    while(j<=nop):
            response=requests.get(f"https://www.google.com/search?q={search_string}&tbm=nws&page={j}/")
            soup=bs(response.text,'html.parser')
            for title in soup.find_all('div',class_='Gx5Zad fP1Qef xpd EtOod pkphOe'):
                    titles.append(title.h3.text)
                    for p in title.find_all('div',class_="BNeawe UPmit AP7Wnd lRVwie"):
                        medias.append(p.text)
                    links.append(title.a['href'])
                    for p in title.find_all('span',class_="r0bn4c rQMQod"):
                        times.append(p.text)
            j+=1
        

    data={"Link":links,"Title":titles,"Source":medias,"Time":times,"Search Engine" :'google',"search String":search_string}
    df=pd.DataFrame(data)
    return df
