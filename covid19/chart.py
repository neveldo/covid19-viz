import plotly
import plotly.graph_objs as go
import json


def create_plot(data, column, column_label='', overlap_column='', overlap_column_label=''):
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
        ],
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
        chart['layout'] = go.Layout(barmode='overlay')

    return json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder)
