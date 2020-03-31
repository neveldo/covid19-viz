import plotly
import plotly.graph_objs as go
import json


def create_plot(data, column):
    if column not in data.columns:
        raise ValueError("Column not found within dataset")

    chart = [
        go.Bar(
            x=data.index,
            y=data[column],
            marker_color='#53762C',
            opacity=0.8
        )
    ]

    return json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder)
