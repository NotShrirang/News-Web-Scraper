import json
import pandas as pd
from google_scraper import Google
from yahoo_scraper import Yahoo
from bing_scraper import Bing
import tqdm


def main():
    json_file = open("config.json")
    data = json.load(json_file)

    for elements in data:
        company_names = elements['company_name']
        keywords = elements['keywords']
        page_count = elements['page_count']

    final_df = pd.DataFrame()
    for company_name in tqdm.tqdm(company_names):
        for keyword in tqdm.tqdm(keywords):
            # google = Google()
            # df1 = google.scrape(company_name, keyword, page_count)
            yahoo = Yahoo()
            df2 = yahoo.scrape(company_name, keyword, page_count)
            # bing = Bing()
            # df3 = bing.scrape(company_name, keyword, page_count)
            # df = pd.concat([df1, df2, df3], ignore_index=True)
            final_df = pd.concat([final_df, df2], ignore_index=True)
    final_df.to_csv('news.csv')


if __name__ == '__main__':
    main()
