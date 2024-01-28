import tqdm
import json


def main():
	with open("config.json",'r') as f:
		data = json.load(f)
	elements = data["query_data"]
	for company_name in tqdm.tqdm(elements['company_names']):
		page_count = elements['page_count']
		for keyword in tqdm.tqdm(elements['keywords']):
			google = Google()
            df1 = google.scrape(company_name, keyword,
                                page_count, base_url=base_urls['google'])
            yahoo = Yahoo()
            df2 = yahoo.scrape(company_name, keyword,
                               page_count, base_url=base_urls['yahoo'])
            bing = Bing()
            df3 = bing.scrape(company_name, keyword,
                              page_count, base_url=base_urls['bing'])
            final_df = pd.concat([final_df, df1, df2, df3], ignore_index=True)
    final_df.to_csv("news.csv")

if __name__ == '__main__':
	main()