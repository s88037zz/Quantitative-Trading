import abc
from datetime import datetime
import numpy as np


class Analysor(metaclass=abc.ABCMeta):
    def __init__(self, data, start_date=None, end_date=None):
        self.start_datetime = self._get_start_datetime(data, start_date)
        self.end_datetime = self._get_end_datetime(data, end_date)
        self._data = self._get_data_in_time(data)

    def _get_data_in_time(self, data):
        return data.loc[(self.start_datetime <= data.datetime) & (data.datetime <= self.end_datetime)].copy()

    def _get_start_datetime(self, data, start_date=None):
        if start_date is None:
            return data.datetime.values[0]
        elif data.datetime.values[0] <= np.datetime64(datetime.strptime(start_date, "%Y/%m/%d")) \
                <= data.datetime.values[-1]:
            return np.datetime64(datetime.strptime(start_date, "%Y/%m/%d"))
        else:
            raise Exception("The start datetime isn't in data")

    def _get_end_datetime(self, data, start_date=None):
        if start_date is None:
            return data.datetime.values[0]
        elif data.datetime.values[0] <= np.datetime64(datetime.strptime(start_date, "%Y/%m/%d")) \
                <= data.datetime.values[-1]:
            return np.datetime64(datetime.strptime(start_date, "%Y/%m/%d"))
        else:
            raise Exception("The start datetime isn't in data")

    @staticmethod
    def get_up_trend_index(directions):
        up_trends = []
        start = None
        for i in range(1, len(directions)):
            if directions[i] == 1 and start is None:
                start = i
            if directions[i] == -1 and (directions[i-1] == 1 or directions[i-1] == 0)and start is not None:
                up_trends.append([start, i-1])
                start = None
        if start is not None:
            up_trends.append([start, len(directions)-1])

        return up_trends

    @staticmethod
    def get_down_trends_index(directions):
        down_trends = []
        start = None
        for i in range(1, len(directions)):
            if directions[i] == -1 and start is None:
                start = i
            if directions[i] == 1 and (directions[i-1] == -1 or directions[i - 1] == 0) and start is not None:
                # add up trend to up trends
                down_trends.append([start, i-1])
                # reset variable of up trend
                start = None
        if start is not None:
            down_trends.append([start, len(directions) - 1])

        return down_trends