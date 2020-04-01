from flask import Flask, render_template
from covid19 import chart
from covid19 import datasource
from datetime import datetime

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    """Main page of the dataviz"""
    ds = datasource.DataSource()
    ds.update_data()

    charts = dict.fromkeys(datasource.DataSource.features)
    for chart_name in charts:
        if chart_name == 'death':
            charts[chart_name] = chart.create_plot(
                ds.data_country,
                chart_name + '_daily',
                'Total',
                chart_name + '_women_daily',
                'Dont femmes'
            )
        else:
            charts[chart_name] = chart.create_plot(
                ds.data_country,
                chart_name + '_daily'
            )

    overall_departments_data, overall_departments_quantiles = ds.get_overall_departments_data_as_json()

    return render_template(
        'index/index.html',
        label='France',
        counters=ds.counters,
        max_date=datetime.strptime(ds.max_date, "%Y-%m-%d").strftime("%d/%m/%Y"),
        charts=charts,
        overall_departments_data=overall_departments_data,
        overall_departments_quantiles=overall_departments_quantiles
    )

@app.route('/departement/<string:department>')
def view_department(department):
    ds = datasource.DataSource()
    ds.update_data()

    data, counters, max_date = datasource.DataSource.get_aggregated_data(ds.data, department)

    charts = dict.fromkeys(datasource.DataSource.features)
    for chart_name in charts:
        if chart_name == 'death':
            charts[chart_name] = chart.create_plot(
                data,
                chart_name + '_daily',
                'Total',
                chart_name + '_women_daily',
                'Dont femmes'
            )
        else:
            charts[chart_name] = chart.create_plot(
                data,
                chart_name + '_daily'
            )

    overall_departments_data, overall_departments_quantiles = ds.get_overall_departments_data_as_json()

    label = ds.get_department_label(department)

    if label == '':
        label = "France"

    return render_template(
        'index/index.html',
        label=label,
        counters=counters,
        max_date=datetime.strptime(max_date, "%Y-%m-%d").strftime("%d/%m/%Y"),
        charts=charts,
        overall_departments_data=overall_departments_data,
        overall_departments_quantiles=overall_departments_quantiles
    )