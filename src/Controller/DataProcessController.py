import numpy as np
import matplotlib.pyplot as plt
import seaborn
from datetime import datetime
import pandas as pd
import os, time


class DataProcessController(object):
    def __init__(self):
        """
        Initialize  PlotController
        :param data: pd.Dataframe
        """
        self.data = None
    """
    For main function that user call.
    """
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
            lambda date: time.mktime(datetime.strptime(date, "%Y年%m月%d日").timetuple()))

    def get_data_summary(self):
        # get value summary need
        start_date = self.get_start_date()
        end_date = self.get_end_date()
        avg_last7 = self.get_avg_last7()
        avg_last30 = self.get_avg_last30()
        avg_last90 = self.get_avg_last90()

        # update summary
        summary = {"start_date": start_date, "end_date": end_date, "avg_last7": avg_last7,
                   "avg_last30": avg_last30, 'avg_last90': avg_last90}

        return summary
    """
    For information of summary.
    """

    def get_start_date(self):
        return self.data.date[self.data.time_series == min(self.data.time_series)].values[0]

    def get_end_date(self):
        return self.data.date[self.data.time_series == max(self.data.time_series)].values[0]

    def get_avg_last7(self):
        pass
    def get_avg_last30(self):
        pass
    def get_avg_last90(self):
        pass
    """
    For function with useful and reuse.
    """
    def get_avg_by_date(self, start, end):
        date = self.data.date.apply(lambda d: datetime.strptime(d, "%Y年%m月%d日"))
        data_in_range = self.data[np.logical_and(date < end, date > start)]
        avg_open = np.average(data_in_range.open)
        avg_close = np.average(data_in_range.close)
        print("from {} to {}, avg open: {}, avg close: {}".format(start, end, avg_open, avg_close))
        return avg_open, avg_close


if __name__ == '__main__':
    data_path = os.path.abspath(os.path.join("..", "..", 'data', "SPY歷史資料.csv"))
    print(data_path)
    ctl = DataProcessController()
    ctl.load(data_path, 'csv')
    ctl.clean_data()