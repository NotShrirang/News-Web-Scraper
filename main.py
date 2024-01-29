import json
import pandas as pd
from scrapers.google_scraper import Google
from scrapers.yahoo_scraper import Yahoo
from scrapers.bing_scraper import Bing
import tqdm
from utils import logger, dataframe_utils, date_utils
import concurrent.futures
import time
import warnings
warnings.filterwarnings("ignore")


def main():

    # fetching data from json file
    with open('config.json', 'r') as f:
        data = json.load(f)
    logger.log_message("SCRAPING BEGINS", level=0)
    base_urls = data['base_url']
    elements = data['query_data']
    print(elements)
    page_count = elements['page_count']
    final_df = pd.DataFrame()
    for company_name in tqdm.tqdm(elements['company_names']):
        logger.log_message("EXEC: Scraping Data for "+company_name, level=0)

        for keyword in tqdm.tqdm(elements['keywords']):
            google = Google()
            yahoo = Yahoo()
            bing = Bing()

            with concurrent.futures.ThreadPoolExecutor() as executor:
            # parallel execution
                futures = [
                    executor.submit(google.scrape, company_name, keyword, page_count, base_url=base_urls['google']),
                    executor.submit(yahoo.scrape, company_name, keyword, page_count, base_url=base_urls['yahoo']),
                    executor.submit(bing.scrape, company_name, keyword, page_count, base_url=base_urls['bing'])
                ]
            # Wait for all tasks to complete
            concurrent.futures.wait(futures)
            # concatenating dataframe
            for future in futures:
                result_df = future.result()
                final_df = pd.concat([final_df, result_df], ignore_index=True)

        logger.log_message("DONE:Scraped Data for "+company_name, level=0)
    logger.log_message("SCRAPING DONE", level=0)
    dataframe_utils.convert_df_to_csv(final_df)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
