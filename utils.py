import datetime
import dateparser
import pandas as pd


def log_message(message:str):
    try:
        with open('scraper.log', 'a') as f:
            f.write(message)
    except Exception as e:
            with open('scraper.log', 'a') as f:
                f.write('Error: ' + str(e.args) + '\n')


def convert_df_to_csv(df: pd.DataFrame):
    df.to_csv('news.csv')


def format_timestamp(timestamp: str):
    return dateparser.parse(str(timestamp))
