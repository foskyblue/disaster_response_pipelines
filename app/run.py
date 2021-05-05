import json

# import joblib
import pandas as pd
import plotly
from util import tokenize
from flask import Flask
from flask import render_template, request
from plotly.graph_objs import Bar, Scatter, Pie
from sqlalchemy import create_engine
from load import load_data, load_model
from figures import load_figures

app = Flask(__name__)

# load data
df = load_data()


# load model
model = load_model()

# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():

    # load figures and ids
    ids, graph_json = load_figures()
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graph_json)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 
    # # load data
    # df = load_data()

    # # load model
    # model = load_model()
    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


@app.route('/html_table')
def html_table():
    return render_template('html_table.html')


def main():
    app.run(host='127.0.0.1', port=5000, debug=True)


if __name__ == '__main__':
    main()