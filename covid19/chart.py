import plotly
import plotly.graph_objs as go
import json

"""
Turns dataframes for covid-19 data into plotly charts 
"""


def create_plot(data, column, column_label='', overlap_column='', overlap_column_label='', chart_type=go.Bar):
    """Returns aggregated data at country or department scale
    Args:
        data: pandas dataframe wich contains the data from data.gouv.fr
        column: column in the dataset from which build the chart
        column_label: label to display in the chart legend for the column
        overlap_column: column name to add on overlapping bar in the chart
        overlap_column_label: label to display in the chart legend for the overlapping column
        chart_type: class of chart to create

    Returns:
        Plotly chart conf as JSON string
    """

    if column not in data.columns:
        raise ValueError("Column not found within dataset")

    chart = {
        'data': [
            chart_type(
                name=column_label,
                x=data.index,
                y=data[column],
                marker_color='#006d2c',
                opacity=0.8
            ),
        ],
        'layout': go.Layout(
            margin=dict(l=30, r=0, b=30, t=20),
        )
    }

    if overlap_column != '':
        chart['data'].append(
            chart_type(
                name=overlap_column_label,
                x=data.index,
                y=data[overlap_column],
                marker_color='#343A40',
                opacity=0.8
            )
        )
        chart['layout'] = go.Layout(
            barmode='overlay',
            legend_orientation="h",
            margin=dict(l=30, r=0, b=30, t=20),
        )

    return json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder)
