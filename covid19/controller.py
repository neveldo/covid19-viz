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

    death_chart = chart.create_plot(ds.data_country, 'death')
    confirmed_chart = chart.create_plot(ds.data_country, 'confirmed')
    resuscitation_chart = chart.create_plot(ds.data_country, 'resuscitation')
    hospitalized_chart = chart.create_plot(ds.data_country, 'hospitalized')
    healed_chart = chart.create_plot(ds.data_country, 'healed')

    return render_template(
        'index/index.html',
        counters=ds.counters,
        max_date=datetime.strptime(ds.max_date, "%Y-%m-%d").strftime("%d/%m/%Y"),
        charts={
            'death_chart': death_chart,
            'confirmed_chart': confirmed_chart,
            'resuscitation_chart': resuscitation_chart,
            'hospitalized_chart': hospitalized_chart,
            'healed_chart': healed_chart,
        }
    )
