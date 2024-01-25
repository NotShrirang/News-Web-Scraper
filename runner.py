import json
import pandas as pd
from google_scraper import Google
from yahoo_scraper import Yahoo
from bing_scraper import Bing
import tqdm
import datetime
import dateparser
import utils


def main():
    # fetching data from json file
    with open('config.json', 'r') as f:
        data = json.load(f)
    utils.log_message("SCRAPING BEGINS\n\n")
    base_urls = data['base_url']
    for elements in tqdm.tqdm(data['query_data']):
        company_name = elements['company_name']
        keywords = elements['keywords']
        page_count = elements['page_count']
        final_df = pd.DataFrame()
        
        utils.log_message("\nEXEC: Scraping Data for "+company_name)
        
        # pass company, keyword and page_count to each search engine function
        for keyword in tqdm.tqdm(keywords):
            google = Google()
            df1 = google.scrape(company_name, keyword, page_count, base_url=base_urls['google'])
            yahoo = Yahoo()
            df2 = yahoo.scrape(company_name, keyword, page_count, base_url=base_urls['yahoo'])
            bing = Bing()
            df3 = bing.scrape(company_name, keyword, page_count, base_url=base_urls['bing'])
            final_df = pd.concat([final_df, df1, df2, df3], ignore_index=True)

        utils.log_message("\nDONE:Scraped Data for "+company_name)
    utils.log_message("\n\nSCRAPING DONE")
    utils.convert_df_to_csv(final_df)


if __name__ == '__main__':
    main()
