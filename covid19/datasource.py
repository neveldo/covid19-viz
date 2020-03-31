import pandas as pd

class DataSource:
    """
    Data module
    """

    SOURCE_URL = 'https://raw.githubusercontent.com/opencovid19-fr/data/master/dist/chiffres-cles.csv'

    def __init__(self):
        self.data_country = pd.DataFrame()
        self.data_departments = pd.DataFrame()
        self.counters = {}
        self.max_date = ''


    def update_data(self):
        """
        Get covid-19 France data from data.gouv.fr
        """
        data = pd.read_csv(DataSource.SOURCE_URL)

        # Extract France data by day
        self.data_country = data.copy()
        self.data_country = self.data_country[(data['granularite'] == 'pays') & (self.data_country['maille_nom'] == 'France')]
        self.data_country = DataSource._format_dataframe(self.data_country)
        self.data_country = self.data_country.groupby('date').max()
        self.data_country = self.data_country.sort_index()


        columns = {
            'confirmed_cumulative': 'confirmed',
            'death_cumulative': 'death',
            'resuscitation_cumulative': 'resuscitation',
            'hospitalized_cumulative': 'hospitalized',
            'healed_cumulative': 'healed',
        }

        self.max_date = self.data_country.index.max()

        for column_cumulative_name, new_column_name in columns.items():
            # Compute daily values instead from cumulative ones
            self.data_country = DataSource._add_daily_data(self.data_country, column_cumulative_name, new_column_name)

            # Compute most recent value for each feature
            self.counters[new_column_name] = self.data_country.at[self.max_date, column_cumulative_name]

        print(self.counters)

        # #####################"

        # Compute departments data
        self.data_departments = data.copy()
        self.data_departments = self.data_departments[(self.data_departments['granularite'] == 'departement')]
        self.data_departments = DataSource._format_dataframe(self.data_departments)
        self.data_departments['entity'] = self.data_departments['entity'].transform(lambda x: x[4:])
        self.data_departments = self.data_departments.groupby('date').max()
        self.data_departments = self.data_departments[pd.notna(self.data_departments['entity'])]

    @staticmethod
    def _format_dataframe(dataframe):
        dataframe = dataframe.loc[:, ['date', 'maille_code', 'cas_confirmes', 'deces', 'reanimation', 'hospitalises', 'gueris']]
        dataframe.columns = ['date', 'entity', 'confirmed_cumulative', 'death_cumulative', 'resuscitation_cumulative', 'hospitalized_cumulative', 'healed_cumulative']
        dataframe = dataframe[dataframe['date'] >= '2020-03-01']

        return dataframe

    @staticmethod
    def _add_daily_data(dataframe, column_cumulative_name, new_column_name):
        cumulative_column = dataframe[column_cumulative_name].copy().reset_index(drop=True)
        cumulative_column_previous_day = dataframe[column_cumulative_name].copy().reset_index(drop=True)
        cumulative_column_previous_day = pd.Series([0]).append(cumulative_column_previous_day, ignore_index=True)
        cumulative_column_previous_day = cumulative_column_previous_day[:-1]

        dataframe[new_column_name] = list(cumulative_column - cumulative_column_previous_day)

        return dataframe

