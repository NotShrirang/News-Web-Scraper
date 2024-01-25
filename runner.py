import json
import pandas as pd
from google_scraper import Google
from yahoo_scraper import Yahoo
from bing_scraper import Bing
import tqdm


def main():
    json_file = open("config.json")
    data = json.load(json_file)
    with open('scraper.log', 'a') as f:
        f.write("#################### SCRAPING BEGUN ####################\n\n")
    for elements in tqdm.tqdm(data):
        company_name = elements['company_name']
        keywords = elements['keywords']
        page_count = elements['page_count']
        final_df = pd.DataFrame()
        with open('scraper.log', 'a') as f:
            f.write("\nEXEC: Scraping Data for "+company_name)
        for keyword in tqdm.tqdm(keywords):
            google = Google()
            df1 = google.scrape(company_name, keyword, page_count)
            yahoo = Yahoo()
            df2 = yahoo.scrape(company_name, keyword, page_count)
            bing = Bing()
            df3 = bing.scrape(company_name, keyword, page_count)
            final_df = pd.concat([final_df, df1, df2, df3], ignore_index=True)
        with open('scraper.log', 'a') as f:
            f.write("\nDONE: Scraped Data for "+company_name)
    with open('scraper.log', 'a') as f:
        f.write("\n\n#################### SCRAPING DONE ####################")
    final_df.to_csv('news.csv')


if __name__ == '__main__':
    main()
