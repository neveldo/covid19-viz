import pandas as pd

"""
Data module
"""
def get_data():
    """
    Get covid-19 France data from data.gouv.fr
    """
    data = pd.read_csv('https://raw.githubusercontent.com/opencovid19-fr/data/master/dist/chiffres-cles.csv')

    # Compute departments data
    data_departments = data.copy()
    data_departments = data_departments[(data_departments['granularite'] == 'departement')]
    data_departments = _clean_data(data_departments)
    data_departments['entity'] = data_departments['entity'].transform(lambda x: x[4:])
    data_departments = data_departments.groupby('date').max()
    data_departments = data_departments[pd.notna(data_departments['entity'])]

    # Compute France data
    data = data[(data['granularite'] == 'pays') & (data['maille_nom'] == 'France')]
    data = _clean_data(data)
    data = data.groupby('date').max()

    return data, data_departments

def _clean_data(data):
    data = data.loc[:, ['date', 'maille_code', 'cas_confirmes', 'deces', 'reanimation', 'hospitalises', 'gueris']]
    data.columns = ['date', 'entity', 'confirmed', 'death', 'resuscitation', 'hospitalized', 'healed']
    data = data[data['date'] >= '2020-03-01']

    return data
