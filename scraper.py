import abc


class Scraper(abc.ABC):
    """abstract class

    Args:
        abc (_type_): _description_
    """
    def scrape(self, company_name: str, keyword: str, page_count: int):

        pass
