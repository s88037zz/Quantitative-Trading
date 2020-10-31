from datetime import datetime
import numpy as np
from src.Controller.Analysis.Analysor import Analysor


class AutomaticOneTwoThree(Analysor):
    def __init__(self, data, start_date, end_date, signal_key='12MA', macd_key="26MA"):
        super().__init__(data, start_date=start_date, end_date=end_date)
        self.signal_key = signal_key
        self.macd_key = macd_key
        self._trends_dict = {}
        self._exceptions = []
        self._status = []

        self.update_directions()
        self.update_trends()

    @property
    def data(self):
        return self._data

    @property
    def trends(self):
        return self._trends

    def analysis(self):
        pass

    def update_directions(self):
        if self.signal_key not in self.data.columns or self.macd_key not in self.data.columns:
            raise Exception("AutomaticOneTwoThree pars error!(signal or macd is not in Dataframe columns.)")
        fast_line = self._data[self.signal_key]
        slow_line = self._data[self.macd_key]
        directions = []
        for f, s in zip(fast_line, slow_line):
            if f > s:
                directions.append(1)
            elif f == s:
                directions.append(0)
            else:
                directions.append(-1)

        self._data['directions'] = directions

    def update_trends(self):
        up_trends = Analysor.get_up_trends(self.data.directions.values)
        down_trends = Analysor.get_down_trends(self.data.directions.values)
        trends = Analysor.get_trends(self.data.directions.values)
        self._up_trends = up_trends
        self._down_trends = down_trends
        self._trends = trends

    def find_highest(self, trend):
        data = self.data.iloc[trend[0]:trend[1], :]
        highest_idx = np.argmax(data.high)
        return data.high.iloc[highest_idx], highest_idx

    def find_lowest(self, trend):
        data = self.data.iloc[trend[0]:trend[1], :]
        lowest_idx = np.argmax(data.low)
        return data.low.iloc[lowest_idx], lowest_idx

