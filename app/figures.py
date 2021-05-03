import json

import joblib
import pandas as pd
import plotly
from plotly.graph_objs import Bar, Scatter, Heatmap
import plotly.graph_objects as px
from sqlalchemy import create_engine


def load_figures():
    """
    :return: Figure containing plots and id for each plot
    """
    engine = create_engine('sqlite:///data/disaster_response.db')
    df = pd.read_sql_table('disaster_response', engine)

    # extract data needed for visuals
    # TODO: modify to extract data for your own visuals
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)

    # co-ordinates for second plot
    columns = list(df.iloc[:, 4:].columns) # get a list of all column names
    columns_value_sum = df.iloc[:, 4:].sum().values # get the sum of all 1's and 0's in each target column
    column_values_0 = (df.iloc[:, 4:]==0).sum().values

    # for a tuple and sort in increasing order of values
    val_tup = [(columns[idx], columns_value_sum[idx], column_values_0[idx]) for idx in range(len(columns))]
    val_tup = sorted(val_tup, key=lambda x: x[1], reverse=False)

    x = [val_tup[idx][0] for idx in range(len(val_tup))]
    y = [val_tup[idx][1] for idx in range(len(val_tup))]    
    y_1 = [val_tup[idx][2] for idx in range(len(val_tup))] 

    # co-ordinates for third plot
    # column_values_0 = (df.iloc[:, 4:]==0).sum().values

    # create visuals
    # TODO: modify to create your own visuals
    graphs = [
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre"
                },
            }
        },

        {
            'data': [
                Bar(
                    x=x,
                    y=y
                )
            ],

            'layout': {
                'title': 'Messages in each category(after data cleaning)',
                'yaxis': {
                    'title': "Number of messages"
                },
                'xaxis': {
                    'title': "Label"
                },
                'xaxis': {'tickangle': -45}
            }
        },

        {
            'data': [
                Heatmap(
                    x=columns,
                    y=columns[::-1],
                    z=df.iloc[:,4:].corr().values
                )
            ],

            'layout': {
                'title': 'Correlation Heatmap of Categories',
                'xaxis': {'tickangle': -45}
            }
        }
    ]

    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graph_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return ids, graph_json