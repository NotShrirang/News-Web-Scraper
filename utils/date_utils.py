import dateparser


def format_timestamp(timestamp: str):
    return dateparser.parse(str(timestamp))
