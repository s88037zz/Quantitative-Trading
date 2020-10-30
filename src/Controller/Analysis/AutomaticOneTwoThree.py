from datetime import datetime
import numpy as np
from src.Controller.Analysis.Analysor import Analysor
class AutomaticOneTwoThree(Analysor):
    def __init__(self, data, start_date, end_date, signal_key='12MA', macd_key="26MA"):
        super().__init__(data, start_date, end_date)
        self.signal_key = signal_key
        self.macd_key = macd_key
        self._trends = {}

        self.update_directions()
        self.update_trends()
        print(self._data.head())

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
        down = Analysor.get_down_trends_index(self.data.directions.values)
        up = Analysor.get_down_trends_index(self.data.directions.values)
        self._trends = {'up_trend': up, "down_trend": down}

