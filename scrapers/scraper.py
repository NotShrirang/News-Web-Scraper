import abc
import pandas as pd


class Scraper(abc.ABC):
    """abstract class

    Args:
        abc (self, company_name: str, keyword: str, page_count: int): scraping code
    """

    def scrape(self, company_name: str, keyword: str, page_count: int, base_url: str) -> pd.DataFrame:

        pass
