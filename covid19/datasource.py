import numpy as np
import pandas as pd
import os
import urllib.request
import json


class DataSource:
    """A Data Source to retrieve and update the covid-19 dataset from data.gouv.fr
    To use :
    >>> ds = DataSource()
    >>> ds.update_data()
    >>> data_country = ds.data_country
    """

    source_url = 'https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7'

    basic_features = ['hospitalized', 'resuscitation', 'death', 'healed']

    def __init__(self):
        self.data = pd.DataFrame()
        self.data_country = pd.DataFrame()
        self.overall_data_departments = pd.DataFrame()
        self.counters = {}
        self.max_date = ""
        self.last_update = ""

        # Init basic departments data
        data_dir = os.path.realpath(os.path.dirname(__file__) + "/../data/")

        self.department_base_data = pd.read_csv(data_dir + "/departments.csv")
        self.department_base_data.index = self.department_base_data['insee']
        self.department_base_data = self.department_base_data.sort_index()

    def update_data(self):
        """Update overall data from data.gouv.fr file"""
        self.data = pd.read_csv(DataSource.source_url, sep=';')
        self.data.columns = ['department', 'sex', 'date'] + DataSource.basic_features
        self.data['date'] = self.data['date'].apply(DataSource.clean_dates)
        self.data = self.data.drop_duplicates()

        self.update_country_data(self.data)
        self.update_overall_departments_data(self.data)

    @staticmethod
    def clean_dates(date):
        """Fix wrong date format"""
        if "/" in date:
            split_date = date.split("/")
            date = split_date[2] + "-" + split_date[1] + "-" + split_date[0]
        return date

    def update_country_data(self, data):
        """Update country data
        Args:
            data: pandas dataframe wich contains the data from data.gouv.fr

        Updates:
            data_country : data aggregated for the country
            counters : overall up-to-date counters for all the features (deaths, etc)
            max_date : max date from the dataset
        """
        self.data_country, self.counters, self.max_date = DataSource.get_aggregated_data(data)

    def update_overall_departments_data(self, data):
        """Update departments overall data
        Args:
            data: pandas dataframe wich contains the data from data.gouv.fr

        Updates:
            overall_data_departments : data aggregated for all departments
        """
        data = data[(data['sex'] == 0)]
        data = data \
            .drop(['date', 'sex'], axis=1) \
            .groupby('department') \
            .max()

        data = pd.concat([data, self.department_base_data], axis=1)

        data['death_per_inhabitants'] = (data['death'] / data['population']) * 100000

        self.overall_data_departments = data

    @staticmethod
    def get_aggregated_data(data, department=""):
        """Returns aggregated data at country or department scale
        Args:
            data: pandas dataframe wich contains the data from data.gouv.fr
            department: to filter on a specific department

        Returns:
            data aggregated for the country or specified department
            overall up-to-date counters for all the features (deaths, etc)
            max date from the dataset
        """
        if department != "" and department in pd.unique(data['department']):
            data = data[(data['department'] == department)]

        # Compute women death
        data_women = data.copy()
        data_women = data_women[(data_women['sex'] == 2)]
        data_women = data_women \
            .drop(['department', 'sex'], axis=1) \
            .groupby('date') \
            .sum() \
            .sort_index()

        data = data[(data['sex'] == 0)]
        data = data \
            .drop(['department', 'sex'], axis=1) \
            .groupby('date') \
            .sum() \
            .sort_index()

        data['death_women'] = data_women['death']

        max_date = data.index.max()

        counters = {}
        for feature in DataSource.basic_features + ['death_women', 'death_daily']:
            # Compute daily counts instead from cumulative ones
            data = DataSource._add_daily_data(data, feature)

            # Compute most recent value for each feature
            counters[feature] = data.at[max_date, feature]

        # Remove first day of data as daily counts will not be valid
        data = data.iloc[1:]

        return data, counters, max_date

    @staticmethod
    def _add_daily_data(data, feature):
        """Add a new column to "data" dataframe wich contains daily values. It is derived from the "feature" column
        that contains cumulative values.
        Args:
            data: pandas dataframe with a "feature" column that contains cumulative values
            feature: column to handle

        Returns:
            data with a new column that contains the daily values for the feature
        """
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
        """Get data from departments as a JSON string along with quantiles

        Returns:
            JSON string of departments overall data
        """
        data = self.overall_data_departments.copy()

        data = data.set_index("department-" + data.index)
        data = data.loc[:, ['label', 'death', 'death_per_inhabitants', 'insee']]

        quantiles = data['death_per_inhabitants'] \
            .quantile([.25, .5, .75, .949]) \
            .round(2)

        data['death_per_inhabitants'] = data['death_per_inhabitants'].round(2)

        return data.to_json(orient='index'), quantiles.to_json(orient='index')

    def get_department_label(self, department):
        """Get a department a department label from its insee code

        Returns:
            Department label
        """
        if department in self.department_base_data.index:
            return self.department_base_data.at[department, 'label']
        return ""

    def need_update(self):
        """Check the last update of the dataset on data.gouv.fr and tells wether we need to refresh the data or not

        Returns:
            True if the data need to be updated, False instead
        """
        with urllib.request.urlopen("https://www.data.gouv.fr/datasets/5e7e104ace2080d9162b61d8/rdf.json") as url:
            data = json.loads(url.read().decode())

            for dataset in data['@graph']:
                if 'accessURL' in dataset.keys() and dataset['accessURL'] == DataSource.source_url:
                    if self.last_update == "" or self.last_update < dataset['modified']:
                        self.last_update = dataset['modified']
                        return True

        return False

if __name__ == "__main__":
    ds = DataSource()
    ds.update_data()
    print(ds.counters)
