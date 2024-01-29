import json
import pandas as pd
from multiprocessing import Pool
from scrapers.google_scraper import Google
from scrapers.yahoo_scraper import Yahoo
from scrapers.bing_scraper import Bing
import tqdm
import timeit
import concurrent.futures
import sys

from utils import logger, dataframe_utils


"""
    iterates over search strings and calls fuctions for scraping

    Args:
        args: consists of base URLs and search strings (company name, keywords, page count)

    Returns:
        pd.DataFrame: will later be converted into csv
"""
def scrape_data_for_company(args):
    elements, base_urls = args
    page_count = elements['page_count']
    final_df = pd.DataFrame()

    logger.log_message(message="EXEC: Scraping Data for " + company_name, level=0)

    # pass company, keyword, and page_count to each search engine function
    for company_name in tqdm.tqdm(elements['company_names']):
        for keyword in tqdm.tqdm(elements['keywords']):
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

    logger.log_message(message="DONE:Scraped Data for " + company_name, level=0)
    return final_df


"""
    scrapes data using multiprocessing

    Args:
        base_urls: base URLs of search engines
        query_data: contains search query data (company name, keywords, page count)
"""
def multiprocessing_module(base_urls, query_data):
    with Pool() as pool:
        # Remove the extra square brackets
        results = list(tqdm.tqdm(pool.imap(scrape_data_for_company, ((
            elements, base_urls) for elements in query_data)), total=len(query_data)))

    final_df = pd.concat(results, ignore_index=True)
    dataframe_utils.convert_df_to_csv(final_df)


"""
    scrapes data using multithreading

    Args:
        base_urls: base URLs of search engines
        query_data: contains search query data (company name, keywords, page count)
"""
def multithreading_module(base_urls, query_data):
   
    page_count = query_data['page_count']
    final_df = pd.DataFrame()

    # pass company, keyword and page_count to each search engine function
    for company_name in tqdm.tqdm(query_data['company_names']):
        logger.log_message(message="EXEC: Scraping Data for "+company_name, level=0)
        for keyword in tqdm.tqdm(query_data['keywords']):
            google = Google()
            yahoo = Yahoo()
            bing = Bing()

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(google.scrape, company_name, keyword,
                                    page_count, base_urls['google']),
                    executor.submit(yahoo.scrape, company_name, keyword,
                                    page_count, base_urls['yahoo']),
                    executor.submit(bing.scrape, company_name, keyword,
                                    page_count, base_urls['bing'])
                ]
            concurrent.futures.wait(futures)

            for future in futures:
                result_df = future.result()
                final_df = pd.concat([final_df, result_df], ignore_index=True)

        logger.log_message(message="DONE:Scraped Data for "+company_name, level=0)
    dataframe_utils.convert_df_to_csv(final_df)


def main():
    start_time = timeit.default_timer()
    # fetching data from json file
    with open('config.json', 'r') as f:
        data = json.load(f)
    logger.log_message(message="SCRAPING BEGINS", level=0)
    base_urls = data['base_url']
    query_data = data['query_data']

    if sys.argv[1] == "multithreading":
        multithreading_module(base_urls=base_urls, query_data=query_data)
    else:
        multiprocessing_module(base_urls=base_urls, query_data=query_data)

    logger.log_message(message="SCRAPING DONE", level=0)

    elapsed_time = timeit.default_timer() - start_time
    logger.log_message(message=f"Elapsed Time: {elapsed_time} seconds", level=0)
    


if __name__ == '__main__':
    main()
