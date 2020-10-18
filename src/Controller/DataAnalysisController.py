import numpy as np
from datetime import datetime, timedelta
class DataAnalysisController(object):
    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        return self._data

    def get_raising_date_ranges(self, his_prices, datetimes):
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

    def get_falling_date_ranges(self, his_prices, datetimes):
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
            print("index:", datetimes[index], his_prices[index], cont_days, falling_range)
        if cont_days != 0:
            falling_range.append(datetimes[len(datetimes)-1])
            falling_ranges.append(falling_range)
        return falling_ranges

if __name__ == '__main__':
    from src.Controller.DataProcessController import DataProcessController
    import os
    # preparing
    path = os.path.abspath(os.path.join("..", "..", 'data', "SPY歷史資料.csv"))
    dp_ctl = DataProcessController(path, 'csv')
    dp_ctl.process()

    # Initialize
    da_ctl = DataAnalysisController(dp_ctl.data)
