from datetime import datetime
import numpy as np
from src.Controller.Analysis.Analysor import Analysor


class AutomaticOneTwoThree(Analysor):
    def __init__(self, data, start_date, end_date, signal_key='12MA', macd_key="26MA", theta=0.05):
        super().__init__(data, start_date=start_date, end_date=end_date)
        self.signal_key = signal_key
        self.macd_key = macd_key
        self.theta = theta

        self.directions = []
        self._trends = {}
        self._up_trends = {}
        self._down_trends = {}
        self._exceptions = []
        self._status = []

        self.last_min_idx = 0
        self.last_max_idx = 0
        self.temp_min_idx = 0
        self.temp_max_idx = 0

        self.init_data_and_property()

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
        # reference index
        for i in range(1, len(self.data)):
            print("Bar index:", i)

            self.init_min_max_process(i)
            self.update_min_max_process(i)
            self.update_exception(i)

            # save this round status
            self.data['last_max_idx'] = self.last_min_idx
            self.data['last_max_idx'] = self.last_max_idx
            self.data['temp_min_idx'] = self.temp_min_idx
            self.data['temp_max_idx'] = self.temp_max_idx

            self._status = np.array(self.directions) * np.array(self._exceptions)

    def init_data_and_property(self):
        self.init_directions()
        self.init_trends()
        self._exceptions = [1 for i in range(len(self.data))]
        self._status = self.directions.copy()
        self.data["last_min_idx"] = np.zeros(len(self.data))
        self.data["last_max_idx"] = np.zeros(len(self.data))
        self.data["temp_max_idx"] = np.zeros(len(self.data))
        self.data['temp_min_idx'] = np.zeros(len(self.data))

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

        self.directions = directions
        self._data['direction'] = self.directions

    def init_trends(self):
        up_trends = Analysor.get_up_trends(self.data.direction.values)
        down_trends = Analysor.get_down_trends(self.data.direction.values)
        trends = Analysor.get_trends(self.data.direction.values)
        self._up_trends = up_trends
        self._down_trends = down_trends
        self._trends = trends

    def get_highest(self, trend):
        """
        找到時間內max height
        :param trend: list, [0]:  date start, [1]: date end
        :return:  max high, relative index of high in time
        """
        data = self.data.iloc[trend[0]:trend[1], :]
        #print("data(high):\n", data.high)
        highest_idx = np.argmax(data.high)
        return data.high.iloc[highest_idx], highest_idx

    def get_lowest(self, trend):
        """
        找到時間內min low
        :param trend: list, [0]:  date start, [1]: date end
        :return:  min low, relative index of low in time
        """
        data = self.data.iloc[trend[0]:trend[1], :]
        #print("data(low):\n", data.low)
        lowest_idx = np.argmin(data.low)
        return data.low.iloc[lowest_idx], lowest_idx

    def get_trend_idx(self, bar_idx):
        for index, trend in enumerate(self.trends):
            if trend[0] <= bar_idx <= trend[1]:
                return index
        return 0

    def init_min_max_process(self, bar_idx):
        trend_idx = self.get_trend_idx(bar_idx)
        directions = self.data.direction.values
        # period of lowest low in previous trend when trend status from -1,0 to 1.
        if directions[bar_idx] == 1 and (directions[bar_idx-1] == 0 or directions[bar_idx-1] == -1):
            lowest, lowest_idx = self.get_lowest(self.trends[trend_idx-1])
            self.last_min_idx = self.trends[trend_idx-1][0] + lowest_idx
            print(" Init last min in", self.data.iloc[bar_idx, :]["date"])

        # period of highest high in previous trend when trend status from 1, 0 to -1.
        if directions[bar_idx] == -1 and (directions[bar_idx-1] == 0 or directions[bar_idx-1] == 1):
            highest, highest_idx = self.get_highest(self.trends[trend_idx-1])
            self.last_max_idx = self.trends[trend_idx-1][0] + highest_idx
            print("  Init last max in", self.data.iloc[bar_idx, :]["date"])

    def update_min_max_process(self, bar_idx):
        print(" Update min max process:")

        bar = self.data.iloc[bar_idx, :]
        # previous bar direction is positive
        if self._status[bar_idx-1] == 1:
            #  current bar high is bigger than temp max high.
            #  (in order to find the max high in this directions)
            if self.data.iloc[self.temp_max_idx]["high"] <= bar["high"]:
                self.temp_max_idx = bar_idx

            # 與前一個的狀態相反，代表occur exception(發生exception時，將資料做個更新)
            if self._status[bar_idx] == -1:
                # end a period
                self.last_max_idx = self.temp_max_idx
                lowest, self.temp_min_idx = self.get_lowest([self.last_min_idx, bar_idx])

        # previous bar direction is negative
        elif self._status[bar_idx-1] == -1:
            if self.data.iloc[self.temp_min_idx, :]["low"] >= bar['low']:
                self.temp_min_idx = bar_idx
            if self._status[bar_idx] == 1:
                self.last_min_idx = self.temp_min_idx
                highest, self.temp_max_idx = self.get_highest([self.last_max_idx, bar_idx])

        # for easy verify
        print("     status[i-1], status[i]:{}, {}"
              "     temp max:{}, "
              "     temp min:{}, "
              "     last max:{}"
              "     last min:{}".format(self._status[bar_idx-1], self._status[bar_idx-1],
                                        self.temp_max_idx, self.temp_min_idx,
                                        self.last_max_idx, self.last_min_idx))

    def update_exception(self, bar_idx):
        bar = self.data.iloc[bar_idx, :]

        last_min = self.data.low.iloc[self.last_min_idx]
        last_max = self.data.high.iloc[self.last_max_idx]

        temp_max = bar.high
        temp_min = bar.low
        cur_direct = bar.direction
        pre_direct = self.data.direction.iloc[bar_idx-1]

        if self._exceptions[bar_idx - 1] == -1:
            #print("     Date(next exception a day):{}".format(row.datetime))
            # exceptional process was already active(如果前一個有Exception的可能, ...)
            if (pre_direct * cur_direct == -1) or \
                    (pre_direct == -1 and last_min >= temp_min) or \
                    (pre_direct == 1 and last_max <= temp_max):
                self._exceptions[bar_idx] = 1
            else:
                self._exceptions[bar_idx] = -1

        elif pre_direct == cur_direct:
            if cur_direct == 1 and last_min >= temp_min:
                print("     find (dir=1) exception in {}".format(bar.datetime))
                self._exceptions[bar_idx] = -1
            elif cur_direct == -1 and last_max <= temp_max:
                print("     find (dir=-1) exception in {}".format(bar.datetime))
                self._exceptions[bar_idx] = -1
            else:
                self._exceptions[bar_idx] = 1

if __name__ == '__main__':
    from src.Controller.Process.DataProcessController import DataProcessController
    import os

    path = os.path.join('..', '..', '..', 'data', 'SPY歷史資料after-2010.csv')
    print(os.path.abspath(path))
    dp_ctl = DataProcessController()
    dp_ctl.process(path, 'csv')
    print("After processing:\n", dp_ctl.data.head())
    aott = AutomaticOneTwoThree(dp_ctl.data,
                                start_date='2017/01/01',
                                end_date='2017/12/31',
                                signal_key='12MA',
                                macd_key='26MA')

    aott.analysis()
    for index, bar in aott.data.iterrows():
        # print(row)
        print("date:{}({}), dir:{}, last_min:{}, last_max:{}".format(bar.date,
                                                                index,
                                                                bar.direction,
                                                                bar['last_min_idx'],
                                                                bar['last_max_idx'],))

