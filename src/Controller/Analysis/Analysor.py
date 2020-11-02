import abc
from datetime import datetime
import numpy as np


class Analysor(metaclass=abc.ABCMeta):
    def __init__(self, data, start_date=None, end_date=None):
        self.start_datetime = self._get_start_datetime(data, start_date)
        self.end_datetime = self._get_end_datetime(data, end_date)
        self._data = self._get_data_in_time(data)

    def _get_data_in_time(self, data):
        sub_data = data.loc[(self.start_datetime <= data.datetime) & (data.datetime <= self.end_datetime)].copy()
        print("Data(Analysor selected):", sub_data.shape)
        return sub_data

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
    def get_up_trends(directions):
        up_trends = []
        star_idx = None
        for i in range(1, len(directions)):
            if directions[i] == -1 and (directions[i-1] == 1 or directions[i-1] == 0) and star_idx is not None:
                up_trends.append([star_idx, i])
                star_idx = None

            if directions[i] == 1 and star_idx is None:
                star_idx = i

        if star_idx is not None:
            up_trends.append([star_idx, len(directions)])

        return up_trends

    @staticmethod
    def get_down_trends(directions):
        down_trends = []
        star_idx = None
        for i in range(0, len(directions)):
            if directions[i] == 1 and (directions[i-1] == -1 or directions[i - 1] == 0) and star_idx is not None:
                down_trends.append([star_idx, i])
                star_idx = None

            if directions[i] == -1 and star_idx is None:
                star_idx = i

        if star_idx is not None:
            down_trends.append([star_idx, len(directions)])

        return down_trends

    @staticmethod
    def get_trends(directions):
        trends = []

        start_idx = None
        d = 0
        for i in range(0, len(directions)):
            if d == -1 and directions[i] == 1 and (directions[i-1] == -1 or directions[i-1] == 0):
                trends.append([start_idx, i]) # down
                start_idx = None
            if d == 1 and directions[i] == -1 and (directions[i-1] == 1 or directions[i-1] == 0):
                trends.append([start_idx, i]) # up
                start_idx = None
            if start_idx is None:
                start_idx = i
                d = directions[i]
        if start_idx is not None:
            trends.append([start_idx, len(directions)])
        return trends






