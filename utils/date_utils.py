# import necessary libraries
import dateparser

def format_timestamp(timestamp: str):
    """
    Formats a timestamp string into a datetime object using dateparser.

    Args:
        timestamp (str): The timestamp string to be formatted.

    Returns:
        datetime.datetime: The formatted datetime object.
    """
    return dateparser.parse(str(timestamp))
