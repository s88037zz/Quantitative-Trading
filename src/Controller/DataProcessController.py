import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import os, time


class DataProcessController(object):
    def __init__(self):
        """
        Initialize  PlotController
        :param data: pd.Dataframe
        """
        self.data = None
        self.date_format = "%Y年%m月%d日"


    """
    For main function that user call.
    """
    def process(self, path, type):
        self.load(path, type)
        self.clean_data()
        self.add_time_series()
        self.add_5MA()
        self.add_20MA()
        self.add_60MA()

    def load(self, path, type):
        if type == "csv":
            self.data = pd.read_csv(path)
        elif type == "json":
            self.data = pd.read_json(path)
        else:
            raise Exception("Loading process not support {}".format(type))

    def clean_data(self):
        columns_map = {'日期': 'date', '收市': 'close', '開市': 'open', '高': 'high',
                       '低': 'low', '成交量': 'volume', '更改%': 'change'}
        # change columns name:
        self.data = self.data.rename(columns=columns_map)
        print(self.data.columns)

        # remove % in change
        self.data.change = self.data.change.apply(lambda value: value.replace('%', ''))

        # remove M in volume
        self.data.volume = self.data.volume.apply(lambda value: value.replace('M', ""))

        # remove the rest day in data frame
        self.data = self.data[self.data.volume != '-']

    def add_time_series(self):
        self.data['time_series'] = self.data.date.apply(
            lambda date: time.mktime(datetime.strptime(date, self.date_format).timetuple()))

    def add_5MA(self):
        self.data["5MA"] = self.data.apply(
            lambda data: self.get_avg_by_date(data.date, 5)[1], axis=1)

    def add_20MA(self):
        self.data["20MA"] = self.data.apply(
            lambda data: self.get_avg_by_date(data.date, 20)[1], axis=1)

    def add_60MA(self):
        self.data["60MA"] = self.data.apply(
            lambda data: self.get_avg_by_date(data.date, 60)[1], axis=1)

    def get_data_summary(self):
        # get value summary need
        start_date = self.get_start_date()
        end_date = self.get_end_date()

        # update summary
        summary = {"start_date": start_date, "end_date": end_date}

        return summary

    """
    For information of summary.
    """
    def get_start_date(self):
        return self.data.date[self.data.time_series == min(self.data.time_series)].values[0]

    def get_end_date(self):
        return self.data.date[self.data.time_series == max(self.data.time_series)].values[0]

    """
    For function with useful and reuse.
    """
    def get_avg_by_date(self, date, delta):
        date_index = int(np.where(self.data.date == date)[0][0])
        if delta > len(self.data) - date_index:
            delta = len(self.data) - date_index

        data = self.data.iloc[date_index: date_index+delta, :]
        avg_open = np.average(data.open)
        avg_close = np.average(data.close)
        return avg_open, avg_close

if __name__ == '__main__':
    data_path = os.path.abspath(os.path.join("..", "..", 'data', "SPY歷史資料.csv"))
    ctl = DataProcessController()

    ctl.process(data_path, 'csv')
    data = ctl.data
    print(data.head())

    # ctl.load(data_path, 'csv')
    # ctl.clean_data()
    # ctl.add_time_series()
    # ctl.get_avg_by_date("2020年9月10日", 10)