import json
import pandas as pd
from scrapers.google_scraper import Google
from scrapers.yahoo_scraper import Yahoo
from scrapers.bing_scraper import Bing
import tqdm
from utils import logger, dataframe_utils, date_utils
import concurrent.futures
import time

def main():
    # fetching data from json file
    with open('config.json', 'r') as f:
        data = json.load(f)
    logger.log_message("SCRAPING BEGINS\n\n", level=0)
    base_urls = data['base_url']
    for elements in tqdm.tqdm(data['query_data']):
        company_name = elements['company_name']
        keywords = elements['keywords']
        page_count = elements['page_count']
        final_df = pd.DataFrame()

        logger.log_message("\nEXEC: Scraping Data for "+company_name, level=0)

        # pass company, keyword and page_count to each search engine function
        for keyword in tqdm.tqdm(keywords):
            google = Google()
            yahoo = Yahoo()
            bing = Bing()
            # google = Google()
            # df1 = google.scrape(company_name, keyword, page_count)
            # yahoo = Yahoo()
            # df2 = yahoo.scrape(company_name, keyword, page_count)
            # bing = Bing()
            # df3 = bing.scrape(company_name, keyword, page_count)
            # final_df = pd.concat([final_df, df1, df2, df3], ignore_index=True)
            with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the functions for parallel execution
                futures = [
                    executor.submit(google.scrape, company_name, keyword, page_count, base_url=base_urls['google']),
                    executor.submit(yahoo.scrape, company_name, keyword, page_count, base_url=base_urls['yahoo']),
                    executor.submit(bing.scrape, company_name, keyword, page_count, base_url=base_urls['bing'])
                ]
            # Wait for all tasks to complete
            concurrent.futures.wait(futures)
            # Get the results
            for future in futures:
                result_df = future.result()
                final_df = pd.concat([final_df, result_df], ignore_index=True)

            # df1 = google.scrape(company_name, keyword,
            #                     page_count, base_url=base_urls['google'])
            # yahoo = Yahoo()
            # df2 = yahoo.scrape(company_name, keyword,
            #                    page_count, base_url=base_urls['yahoo'])
            # bing = Bing()
            # df3 = bing.scrape(company_name, keyword,
            #                   page_count, base_url=base_urls['bing'])
            # final_df = pd.concat([final_df, df1, df2, df3], ignore_index=True)

        logger.log_message("\nDONE:Scraped Data for "+company_name, level=0)
    logger.log_message("\n\nSCRAPING DONE", level=1)
    dataframe_utils.convert_df_to_csv(final_df)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
