import plotly
import plotly.graph_objs as go
import json

"""
Turns dataframes for covid-19 data into plotly charts 
"""


def create_plot(data, column, column_label='', overlap_column='', overlap_column_label=''):
    """Returns aggregated data at country or department scale
    Args:
        data: pandas dataframe wich contains the data from data.gouv.fr
        column: column in the dataset from which build the chart
        column_label: label to display in the chart legend for the column
        overlap_column: column name to add on overlapping bar in the chart
        overlap_column_label: label to display in the chart legend for the overlapping column

    Returns:
        Plotly chart conf as JSON string
    """

    if column not in data.columns:
        raise ValueError("Column not found within dataset")

    chart = {
        'data': [
            go.Bar(
                name=column_label,
                x=data.index,
                y=data[column],
                marker_color='#006d2c',
                opacity=0.8
            ),
        ]
    }

    if overlap_column != '':
        chart['data'].append(
            go.Bar(
                name=overlap_column_label,
                x=data.index,
                y=data[overlap_column],
                marker_color='#343A40',
                opacity=0.8
            )
        )
        chart['layout'] = go.Layout(
            barmode='overlay',
            legend_orientation="h"
        )

    return json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder)
