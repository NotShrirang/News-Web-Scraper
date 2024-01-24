import abc


class Scraper(abc.ABC):
    def scrape(self, company_name: str, keyword: str, page_count: int):
        pass
