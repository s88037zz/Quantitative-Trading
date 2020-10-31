import numpy as np
from src.Controller.Analysis.AutomaticOneTwoThree import AutomaticOneTwoThree

class DataAnalysisController(object):
    def __init__(self, data):
        self._data = data
        self.autt_analysor = AutomaticOneTwoThree(data)

    @property
    def data(self):
        return self._data


if __name__ == '__main__':
    pass
    # from src.Controller.Process.DataProcessController import DataProcessController
    # import os
    # # preparing
    # path = os.path.abspath(os.path.join("../..", "..", 'data', "SPY歷史資料.csv"))
    # # path= os.path.abspath(os.path.join("..", "..", 'data', "SPY歷史資料 (3 months).csv"))
    # dp_ctl = DataProcessController()
    # dp_ctl.process(path, 'csv')
    #
    # # Initialize class and parameters
    # da_ctl = DataAnalysisController(dp_ctl.data)
    # prices = dp_ctl.data['close']
    # ma5 = dp_ctl.data['5MA']
    # datetimes = dp_ctl.data['datetime']
    #
    # # get raised and fallen
    # raising_trend = da_ctl.get_raising_labels(ma5, datetimes)
    # falling_trend = da_ctl.get_falling_labels(ma5, datetimes)
    # trend_labels = da_ctl.get_trend_labels(ma5, datetimes)
    #
    # # get labes to show two prices witich is higher than anther
    # trends = da_ctl.get_relative_of_prices(prices, ma5)
    # print(trends)