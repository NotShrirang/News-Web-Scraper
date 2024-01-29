import json
import pandas as pd
from multiprocessing import Pool
from scrapers.google_scraper import Google
from scrapers.yahoo_scraper import Yahoo
from scrapers.bing_scraper import Bing
import tqdm
import timeit

from utils import logger, dataframe_utils, date_utils


def scrape_data_for_company(args):
    elements, base_urls = args
    company_name = elements['company_name']
    keywords = elements['keywords']
    page_count = elements['page_count']
    final_df = pd.DataFrame()

    logger.log_message("\nEXEC: Scraping Data for " + company_name)

    # pass company, keyword, and page_count to each search engine function
    for keyword in tqdm.tqdm(keywords):
        google = Google()
        df1 = google.scrape(company_name, keyword, page_count,
                            base_url=base_urls['google'])
        yahoo = Yahoo()
        df2 = yahoo.scrape(company_name, keyword, page_count,
                           base_url=base_urls['yahoo'])
        bing = Bing()
        df3 = bing.scrape(company_name, keyword, page_count,
                          base_url=base_urls['bing'])
        final_df = pd.concat([final_df, df1, df2, df3], ignore_index=True)

    logger.log_message("\nDONE:Scraped Data for " + company_name)
    return final_df


def main():
    start_time = timeit.default_timer()
    # fetching data from json file
    with open('config.json', 'r') as f:
        data = json.load(f)
    logger.log_message("SCRAPING BEGINS\n\n")
    base_urls = data['base_url']
    query_data = data['query_data']

    with Pool() as pool:
        # Remove the extra square brackets
        results = list(tqdm.tqdm(pool.imap(scrape_data_for_company, ((
            elements, base_urls) for elements in query_data)), total=len(query_data)))

    final_df = pd.concat(results, ignore_index=True)
    logger.log_message("\n\nSCRAPING DONE")
    elapsed_time = timeit.default_timer() - start_time
    logger.log_message(f"Elapsed Time: {elapsed_time} seconds")
    dataframe_utils.convert_df_to_csv(final_df)


if __name__ == '__main__':
    main()
