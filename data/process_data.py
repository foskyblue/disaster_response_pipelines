import sys
import pandas as pd
import sqlite3
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath):
    """
    :param messages_filepath: file path for messages file in csv format
    :param categories_filepath: file path for message categories file in csv format
    :return: merged message and categories dataframe
    """
    # read data
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)

    # merge both data sets
    df = pd.merge(messages, categories)
    return df


def clean_data(df):
    """
    :param df: merged message and categories dataframe
    :return: cleaned dataframe
    """
    # create a dataframe of the 36 individual category columns
    categories = df['categories'].str.split(';', expand=True)
    row = categories.iloc[0]  # select the first row of the categories dataframe

    # use this row to extract a list of new column names for categories.
    category_col_names = row.apply(lambda x: x[:-2])
    categories.columns = category_col_names

    # Convert category values to just numbers 0 or 1
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].apply(lambda x: x[-1])

        # convert column from string to numeric
        categories[column] = categories[column].apply(pd.to_numeric)

    # replace all 2's with 1's in the target column named 'related'.
    categories.loc[categories['related'] == 2, 'related'] = 1
    categories['related'].unique()

    # Replace categories column in df with new category columns.
    df = df.drop('categories', axis=1)
    df = pd.concat([df, categories], axis=1)

    # Remove duplicates
    df.drop_duplicates(inplace=True)
    return df


def save_data(df, database_filename):
    """
    :param df: cleaned dataframe
    :param database_filename: name of database when saved
    :return: None
    """
    if '.' in database_filename:
        database_filename = database_filename.split('.')[0]
    
    engine = create_engine('sqlite:///'+database_filename+'.db')
    table_name = database_filename.split('/')[1]
    df.to_sql(table_name, engine, index=False, if_exists="replace")


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
