import pandas as pd


def convert_df_to_csv(df: pd.DataFrame):
    df.to_csv('news.csv')
