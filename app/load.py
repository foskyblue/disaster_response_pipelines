import joblib
import pandas as pd
from sqlalchemy import create_engine


def load_data():
    """
    :return: Data frame
    """
    # load data
    engine = create_engine('sqlite:///data/disaster_response.db')
    df = pd.read_sql_table('disaster_response', engine)
    return df


def load_model():
    """
    :return: Pickled file used for prediction
    """
    # load model
    model = joblib.load("models/disaster_response_pickle.pkl")

    return model