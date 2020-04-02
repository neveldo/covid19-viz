from flask import Flask, render_template
from covid19 import chart
from covid19 import datasource
from datetime import datetime

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
    charts = dict.fromkeys(datasource.DataSource.features)
    for chart_name in charts:
        if chart_name == 'death':
            charts[chart_name] = chart.create_plot(
                data,
                chart_name + "_daily",
                "Total",
                chart_name + "_women_daily",
                "Dont femmes"
            )
        else:
            charts[chart_name] = chart.create_plot(
                data,
                chart_name + "_daily"
            )
    return charts
