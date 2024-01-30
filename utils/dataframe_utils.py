# import necessary libraries
import pandas as pd

def convert_df_to_csv(df: pd.DataFrame):
    """
    Converts a DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to be converted.

    Returns:
        None: The CSV file is saved with the name 'news.csv'.
    """
    df.to_csv('news.csv')
