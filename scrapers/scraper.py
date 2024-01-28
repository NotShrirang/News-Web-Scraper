import abc


class Scraper(abc.ABC):
    """abstract class

    Args:
        abc (self, company_name: str, keyword: str, page_count: int): scraping code
    """
    def scrape(self, company_name: str, keyword: str, page_count: int):

        pass
