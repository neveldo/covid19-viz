from flask import Flask, render_template
from covid19 import chart
from covid19 import datasource

app = Flask(__name__, template_folder='../templates', static_folder='../static')


@app.route('/')
def index():
    """Main page of the dataviz"""
    data_country, data_departments = datasource.get_data()

    death_chart = chart.create_plot(data_country, 'death')
    confirmed_chart = chart.create_plot(data_country, 'confirmed')
    resuscitation_chart = chart.create_plot(data_country, 'resuscitation')
    hospitalized_chart = chart.create_plot(data_country, 'hospitalized')
    healed_chart = chart.create_plot(data_country, 'healed')

    return render_template(
        'index/index.html',
        charts={
            'death_chart': death_chart,
            'confirmed_chart': confirmed_chart,
            'resuscitation_chart': resuscitation_chart,
            'hospitalized_chart': hospitalized_chart,
            'healed_chart': healed_chart,
        }
    )
