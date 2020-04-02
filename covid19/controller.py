from flask import Flask, render_template
from covid19 import chart
from covid19 import datasource
from datetime import datetime
import plotly.graph_objs as go

"""
Main app controller
"""
app = Flask(__name__, template_folder='../templates', static_folder='../static')


@app.route('/')
def index():
    """Country page of the app"""
    ds = datasource.DataSource()
    if ds.need_update():
        ds.update_data()

    charts = _get_charts(ds.data_country)
    overall_departments_data, overall_departments_quantiles = ds.get_overall_departments_data_as_json()

    return render_template(
        "index/index.html",
        label="France",
        department='',
        counters=ds.counters,
        max_date=datetime.strptime(ds.max_date, "%Y-%m-%d").strftime("%d/%m/%Y"),
        last_update=datetime.strptime(ds.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y à %H:%M"),
        charts=charts,
        overall_departments_data=overall_departments_data,
        overall_departments_quantiles=overall_departments_quantiles
    )


@app.route('/departement/<string:department>')
def view_department(department):
    """Department page of the app"""
    ds = datasource.DataSource()
    if ds.need_update():
        ds.update_data()

    data, counters, max_date = datasource.DataSource.get_aggregated_data(ds.data, department)
    charts = _get_charts(data)
    overall_departments_data, overall_departments_quantiles = ds.get_overall_departments_data_as_json()

    label = ds.get_department_label(department)
    if label == "":
        label = "France"
        department = ""

    return render_template(
        "index/index.html",
        label=label,
        department=department,
        counters=counters,
        max_date=datetime.strptime(max_date, "%Y-%m-%d").strftime("%d/%m/%Y"),
        last_update=datetime.strptime(ds.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y à %H:%M"),
        charts=charts,
        overall_departments_data=overall_departments_data,
        overall_departments_quantiles=overall_departments_quantiles
    )


def _get_charts(data):
    """Get plotly charts collection for the available features
    Returns:
        dict that contains chart confs as JSON strings
    """

    charts = [
        {'column': 'hospitalized', 'chart_type': go.Scatter, 'chart_options': {'line_shape': 'spline'}},
        {'column': 'resuscitation', 'chart_type': go.Scatter, 'chart_options': {'line_shape': 'spline'}},
        {'column': 'healed_daily'},
        {'column': 'death_daily', 'column_label': 'Total', 'overlap_column': 'death_women_daily', 'overlap_column_label': 'Dont femmes'},
        {'column': 'death', 'column_label': 'Total', 'overlap_column': 'death_women', 'overlap_column_label': 'Dont femmes'},
    ]

    json_charts = {}
    for chart_conf in charts:
        json_charts[chart_conf['column']] = chart.create_plot(
            data=data,
            **chart_conf
        )
    return json_charts
