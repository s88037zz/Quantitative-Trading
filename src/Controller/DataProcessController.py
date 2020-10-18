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
        self._data = None
        self._date_format = "%Y年%m月%d日"
        self._summary = None
        self._start_date = None
        self._end_date = None

    """
    For getter and setter
    """

    @property
    def data(self):
        return self._data

    @property
    def summary(self):
        # update summary
        self._summary = {"start_date": self.start_date, "end_date": self.end_date}
        return self._summary

    @property
    def start_date(self):
        self._start_date = self.data.date[self.data.time_series == min(self.data.time_series)].values[0]
        return self._start_date

    @property
    def end_date(self):
        self._end_date = self.data.date[self.data.time_series == max(self.data.time_series)].values[0]
        return self._end_date

    @property
    def ma5(self):
        return self.data['5MA']

    @property
    def ma20(self):
        return self.data['20MA']

    @property
    def ma60(self):
        return self.data['60MA']

    """
    For main function that user call.
    """
    def process(self, path, type):
        self.load(path, type)
        self.clean_data()
        self.add_time_series()
        self.sorted_by_time_series()
        self.add_5MA()
        self.add_20MA()
        self.add_60MA()
        self.add_datetime()


    def load(self, path, type):
        if type == "csv":
            self._data = pd.read_csv(path)
        elif type == "json":
            self._data = pd.read_json(path)
        else:
            raise Exception("Loading process not support {}".format(type))

    def clean_data(self):
        columns_map = {'日期': 'date', '收市': 'close', '開市': 'open', '高': 'high',
                       '低': 'low', '成交量': 'volume', '更改%': 'change'}
        # change columns name:
        self._data = self.data.rename(columns=columns_map)
        print(self.data.columns)

        # remove % in change
        self.data.change = self.data.change.apply(lambda value: value.replace('%', ''))

        # remove M in volume
        self.data.volume = self.data.volume.apply(lambda value: value.replace('M', ""))

        # remove the rest day in data frame
        self._data = self.data[self.data.volume != '-']

    def sorted_by_time_series(self):
        self._data = self._data.sort_values(by=['time_series'], ascending=True)
        self._data = self._data.reset_index()
    def add_datetime(self):
        self.data['datetime'] = self.data.apply(lambda d: datetime.strptime(d.date, self._date_format), axis=1)

    def add_time_series(self):
        self.data['time_series'] = self.data.date.apply(
            lambda d: time.mktime(datetime.strptime(d, self._date_format).timetuple()))

    def add_5MA(self):
        self.data["5MA"] = self.data.apply(
            lambda d: self.get_avg_by_date(d.date, 5)[1], axis=1)

    def add_20MA(self):
        self.data["20MA"] = self.data.apply(
            lambda d: self.get_avg_by_date(d.date, 20)[1], axis=1)

    def add_60MA(self):
        self.data["60MA"] = self.data.apply(
            lambda d: self.get_avg_by_date(d.date, 60)[1], axis=1)

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

    print(ctl.data['datetime'])