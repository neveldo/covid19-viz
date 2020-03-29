import plotly
import plotly.graph_objs as go
import json


def create_plot(data, column):
    if column not in data.columns:
        raise ValueError("Column not found within dataset")

    chart = [
        go.Scatter(
            x=data.index,
            y=data[column],
            mode='lines+markers',
            line_color='#53762C',
            opacity=0.8,
            connectgaps=True
        )
    ]

    return json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder)
