import sys
import nltk

nltk.download(['punkt', 'wordnet', 'averaged_perceptron_tagger'])

import re
import numpy as np
import pandas as pd
import sqlite3
from util import Utility, tokenize
from sqlalchemy import create_engine
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

import pickle
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


def load_data(database_filepath):
    """
    :param database_filepath: file path of data to be loaded
    :return: training data dataframe, target columns dataframe and target column names
    """
    engine = sqlite3.connect(database_filepath)
    df = pd.read_sql("SELECT * FROM disaster_response", engine)
    X = df['message'].values
    Y = df[df.columns[4:]]
    categories = Y.columns
    return X, Y, categories


def build_model():
    """
    :param : None
    :return: Grid search model pipeline
    """
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(RandomForestClassifier()))
    ])

    # parameters = {
    #     "clf": [RandomForestClassifier()],
    #     'tfidf__use_idf': (True, False),
    #     "clf__n_estimators": [10, 100, 250],
    #     'clf__min_samples_split': [2, 4, 10],
    # }

    parameters = {
        "clf": [RandomForestClassifier()],
        # 'tfidf__use_idf': [False],
        "clf__n_estimators": [10],
        'clf__min_samples_split': [2],
    }

    cv = GridSearchCV(pipeline, param_grid=parameters)
    return cv


def evaluate_model(model, X_test, Y_test, category_names):
    """
    :param model: Grid search model pipeline to be used for prediction and evaluation
    :param X_test: test data sets
    :param Y_test: test data sets target columns to evaluate classifier
    :param category_names: test data column names
    :return: None
    """
    y_pred_cv = model.predict(X_test)
    # print('Best parameters: ', model.best_params_)
    Y_test = np.array(Y_test)
    for idx in range(36):
        print(classification_report(Y_test[:, idx], y_pred_cv[:, idx]))
        print()


def save_model(model, model_filepath):
    """
    :param model: Grid search model pipeline
    :param model_filepath: file path where model will be saved
    :return: None
    """
    pkl_filename = model_filepath
    with open(pkl_filename, 'wb') as file:
        pickle.dump(model, file)


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        print('Building model...')
        model = build_model()

        print('Training model...')
        model.fit(X_train, Y_train)

        print('Best params ', model.best_params_)

        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database ' \
              'as the first argument and the filepath of the pickle file to ' \
              'save the model to as the second argument. \n\nExample: python ' \
              'train_classifier.py ../data/disaster_response.db disaster_response_pickle.pkl')


if __name__ == '__main__':
    main()
