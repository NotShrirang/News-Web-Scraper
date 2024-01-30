# import necessary libraries
import abc
import pandas as pd


class Scraper(abc.ABC):
    """
    Abstract base class for scrapers

    Args:
        abc (self, company_name: str, keyword: str, page_count: int): scraping code
    """

    @abc.abstractmethod
    def scrape(self, company_name: str, keyword: str, page_count: int, base_url: str) -> pd.DataFrame:
        """
        Abstract method to be implemented by subclasses for scraping data.

        Args:
            company_name (str): Name of the company.
            keyword (str): Extra word to be searched along with the company name.
            page_count (int): Number of pages to be searched.
            base_url (str): Base URL for constructing search requests.

        Returns:
            pd.DataFrame: Data scraped from the specified source.
        """

        pass
