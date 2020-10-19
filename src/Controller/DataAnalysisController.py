import numpy as np
from datetime import datetime, timedelta
class DataAnalysisController(object):
    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        return self._data

    def get_raising_date(self, his_prices, datetimes):
        raising_ranges = []
        raising_range = []
        cont_days = 0
        start_index = 0
        for index in range(1, len(his_prices)):
            if his_prices.iloc[index] >= his_prices.iloc[index-1]:
                if len(raising_range) == 0:
                    start_index = index - 1
                    raising_range.append(datetimes[start_index])
                cont_days += 1
            else:
                if len(raising_range) != 0:
                    raising_range.append(datetimes[start_index+cont_days])
                    raising_ranges.append(raising_range)
                raising_range = []
                cont_days = 0
        if cont_days != 0:
            raising_range.append(datetimes[len(datetimes)-1])
            raising_ranges.append(raising_range)
        return raising_ranges

    def get_falling_date(self, his_prices, datetimes):
        falling_ranges = []
        falling_range = []
        cont_days = 0
        start_index = 0
        for index in range(1, len(his_prices)):
            if his_prices.iloc[index] <= his_prices.iloc[index-1]:
                if len(falling_range) == 0:
                    start_index = index - 1
                    falling_range.append(datetimes[start_index])
                cont_days += 1
            else:
                if len(falling_range) != 0:
                    falling_range.append(datetimes[start_index+cont_days])
                    falling_ranges.append(falling_range)
                falling_range = []
                cont_days = 0

        if cont_days != 0:
            falling_range.append(datetimes[len(datetimes)-1])
            falling_ranges.append(falling_range)
        return falling_ranges

    def get_trend_labels(self, his_prices, datetimes):
        raising_trend = self.get_raising_labels(his_prices, datetimes)
        falling_trend = self.get_falling_labels(his_prices, datetimes)
        trend_labels = raising_trend + falling_trend
        for index, trend in enumerate(trend_labels):
            if trend == 0:
                trend_labels[index] = trend_labels[index-1]
        return trend_labels

    def get_raising_labels(self, his_prices, datetimes):
        trend = np.zeros(len(datetimes)-1)
        for index in range(1, len(datetimes)):
            if his_prices[index] >= his_prices[index-1]:
                trend[index-1] = 1
        return trend

    def get_falling_labels(self, his_prices, datetimes):
        trend = np.zeros(len(datetimes)-1)
        for index in range(1, len(datetimes)):
            if his_prices[index] <= his_prices[index-1]:
                trend[index-1] = -1
        return trend


if __name__ == '__main__':
    from src.Controller.DataProcessController import DataProcessController
    import os
    # preparing
    path = os.path.abspath(os.path.join("..", "..", 'data', "SPY歷史資料.csv"))
    dp_ctl = DataProcessController()
    dp_ctl.process(path, 'csv')

    # Initialize
    da_ctl = DataAnalysisController(dp_ctl.data)
    prices = dp_ctl.data['5MA']
    datetimes = dp_ctl.data['datetime']
    raising_trend = da_ctl.get_raising_labels(prices, datetimes)
    falling_trend = da_ctl.get_falling_labels(prices, datetimes)

    trend_labels = da_ctl.get_trend_labels(prices, datetimes)

    # for d, r, f, t in zip(datetimes[1:], raising_trend, falling_trend, trend_labels):
    #     print("datetime:{}, raisied:{}, falled:{}, trend:{}".format(d, r, f, t))