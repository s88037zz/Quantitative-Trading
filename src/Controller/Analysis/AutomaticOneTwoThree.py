from datetime import datetime
import numpy as np
from src.Controller.Analysis.Analysor import Analysor


class AutomaticOneTwoThree(Analysor):
    def __init__(self, data, start_date, end_date, signal_key='12MA', macd_key="26MA", theta=0.05):
        super().__init__(data, start_date=start_date, end_date=end_date)
        self.signal_key = signal_key
        self.macd_key = macd_key
        self.theta = theta

        self._trends = {}
        self._up_trends = {}
        self._down_trends = {}
        self._exceptions = np.zeros(data.shape[0])
        self._status = []

        self.init_directions()
        self.init_trends()
        self.init_min_max_process()

    @property
    def data(self):
        return self._data

    @property
    def trends(self):
        return self._trends

    @property
    def up_trends(self):
        return self._up_trends

    @property
    def down_trends(self):
        return self._down_trends

    def analysis(self):
        pass

    def init_directions(self):
        if self.signal_key not in self.data.columns or self.macd_key not in self.data.columns:
            raise Exception("AutomaticOneTwoThree pars error!(signal or macd is not in Dataframe columns.)")
        fast_line = self._data[self.signal_key]
        slow_line = self._data[self.macd_key]
        directions = []
        for fast, slow in zip(fast_line, slow_line):
            if fast > slow:
                directions.append(1)
            elif fast == slow:
                directions.append(0)
            else:
                directions.append(-1)

        self._data['directions'] = directions

    def init_trends(self):
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
        lowest_idx = np.argmin(data.low)
        return data.low.iloc[lowest_idx], lowest_idx

    def init_min_max_process(self):
        directions = self.data.directions.values
        last_min_idx = 0
        last_max_idx = 0
        last_min_idx_list = []
        last_max_idx_list = []
        trend_idx = 0
        for i in range(0, len(directions)):
            if i not in range(self.trends[trend_idx][0], self.trends[trend_idx][1]):
                trend_idx += 1

            if directions[i] == 1 and (directions[i-1] == 0 or directions[i-1] == -1):
                lowest, lowest_idx = self.find_lowest(self.trends[trend_idx-1])
                last_min_idx = self.trends[trend_idx-1][0] + lowest_idx

            if directions[i] == -1 and (directions[i-1] == 0 or directions[i-1] == 1):
                highest, highest_idx = self.find_highest(self.trends[trend_idx-1])
                last_max_idx = self.trends[trend_idx-1][0] + highest_idx

            last_min_idx_list.append(last_min_idx)
            last_max_idx_list.append(last_max_idx)

        self.data["last_min_idx"] = last_min_idx_list
        self.data["last_max_idx"] = last_max_idx_list

    def update_exceptions(self):
        print("Exception:")
        directions = self.data.directions.values
        for i in range(len(directions)):
            # for i == 0

            last_min_idx = self.data.last_min_idx.iloc[i]
            last_min = self.data.low.iloc[last_min_idx]
            last_max_idx = self.data.last_max_idx.iloc[i]
            last_max = self.data.high.iloc[last_max_idx]

            row = self.data.iloc[i, :]
            temp_max = row.high
            temp_min = row.low
            cur_direct = row.directions
            pre_direct = self.data.directions.iloc[i-1]

            if self._exceptions[i - 1] == -1:
                #print("     Date(next exception a day):{}".format(row.datetime))
                # exceptional process was already active(如果前一個有Exception的可能, ...)
                if (pre_direct * cur_direct == -1) or \
                        (pre_direct == -1 and last_min >= temp_min) or \
                        (pre_direct == 1 and last_max <= temp_max):
                    self._exceptions[i] = 1
                else:
                    self._exceptions[i] = -1
            elif pre_direct == cur_direct:
                if cur_direct == 1 and last_min >= temp_min:
                    print(" Data:{}".format(row.datetime))
                    self._exceptions[i] = -1
                elif cur_direct == -1 and last_max <= temp_max:
                    print(" Data:{}".format(row.datetime))
                    self._exceptions[i] = -1
                else:
                    self._exceptions[i] = 1

if __name__ == '__main__':
    from src.Controller.Process.DataProcessController import DataProcessController
    import os

    path = os.path.join('..', '..', '..', 'data', 'SPY歷史資料after-2010.csv')
    print(os.path.abspath(path))
    dp_ctl = DataProcessController()
    dp_ctl.process(path, 'csv')
    aott = AutomaticOneTwoThree(dp_ctl.data,
                                start_date='2017/01/01',
                                end_date='2017/12/31',
                                signal_key='12MA',
                                macd_key='26MA')
