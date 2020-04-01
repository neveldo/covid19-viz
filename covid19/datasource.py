import numpy as np
import pandas as pd
import os

class DataSource:
    """
    Data module
    """

    source_url = 'https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7'

    features = ['hospitalized', 'resuscitation', 'healed', 'death']

    def __init__(self):
        self.data = pd.DataFrame()
        self.data_country = pd.DataFrame()
        self.overall_data_departments = pd.DataFrame()
        self.counters = {}
        self.max_date = ''

        data_dir = os.path.realpath(os.path.dirname(__file__) + "/../data/")

        self.department_base_data = pd.read_csv(data_dir + "/departments.csv")
        self.department_base_data.index = self.department_base_data['insee']
        self.department_base_data = self.department_base_data.sort_index()

    def update_data(self):
        """
        Get covid-19 France data from data.gouv.fr
        """
        self.data = pd.read_csv(DataSource.source_url, sep=';')
        self.data.columns = ['department', 'sex', 'date'] + DataSource.features

        self.update_country_data(self.data)
        self.update_overall_departments_data(self.data)

    def update_country_data(self, data):
        self.data_country, self.counters, self.max_date = DataSource.get_aggregated_data(data)

    @staticmethod
    def get_aggregated_data(data, department=""):

        if department != "" and department in pd.unique(data['department']):
            data = data[(data['department'] == department)]

        # Compute women death
        data_women = data.copy()
        data_women = data_women[(data_women['sex'] == 2)]
        data_women = data_women\
            .drop(['department', 'sex'], axis=1)\
            .groupby('date')\
            .sum()\
            .sort_index()

        data = data[(data['sex'] == 0)]
        data = data\
            .drop(['department', 'sex'], axis=1)\
            .groupby('date')\
            .sum()\
            .sort_index()

        data['death_women'] = data_women['death']

        max_date = data.index.max()

        counters = {}
        for feature in DataSource.features + ['death_women']:
            # Compute daily counts instead from cumulative ones
            data = DataSource._add_daily_data(data, feature)

            # Compute most recent value for each feature
            counters[feature] = data.at[max_date, feature]

        # Remove first day of data as daily counts will not be valid
        data = data.iloc[1:]

        return data, counters, max_date

    def update_overall_departments_data(self, data):
        data = data[(data['sex'] == 0)]
        data = data\
            .drop(['date', 'sex'], axis=1)\
            .groupby('department')\
            .max()

        data = pd.concat([data, self.department_base_data], axis=1)

        data['death_per_inhabitants'] = (data['death'] / data['population']) * 100000

        self.overall_data_departments = data

    @staticmethod
    def _add_daily_data(data, feature):
        new_feature = feature + '_daily'

        cumulative_column = data[feature].copy().reset_index(drop=True)

        cumulative_column_previous_day = data[feature].copy().reset_index(drop=True)
        cumulative_column_previous_day = pd.Series([0]).append(cumulative_column_previous_day, ignore_index=True)
        cumulative_column_previous_day = cumulative_column_previous_day[:-1]

        daily_data = np.array(cumulative_column - cumulative_column_previous_day)
        daily_data[daily_data < 0] = 0
        data[new_feature] = daily_data

        return data

    def get_overall_departments_data_as_json(self):
        data = self.overall_data_departments.copy()

        data = data.set_index("department-" + data.index)
        data = data.loc[:, ['label', 'death', 'death_per_inhabitants', 'insee']]

        quantiles = data['death_per_inhabitants']\
            .quantile([.2,.4,.6,.8]) \
            .round(2)

        data['death_per_inhabitants'] = data['death_per_inhabitants'].round(2)

        return data.to_json(orient='index'), quantiles.to_json(orient='index')

    def get_department_label(self, department):
        if department in self.department_base_data.index:
            return self.department_base_data.at[department, 'label']
        return ""


if __name__ == "__main__":
    ds = DataSource()
    ds.update_data()
