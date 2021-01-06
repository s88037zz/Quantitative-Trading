import numpy as np
from src.Controller.Analysis.Analysor import Analysor


class AutomaticOneTwoThree(Analysor):
    def __init__(self, data, start_date, end_date, signal_key='12MA', macd_key="26MA", theta=0.05):
        super().__init__(data, start_date=start_date, end_date=end_date)
        self.signal_key = signal_key
        self.macd_key = macd_key
        self.theta = theta

        self.directions = [] # len is the same at data
        self._trends = []
        self._up_trends = []
        self._down_trends = []
        self._exceptions = []
        self._status = []

        self.last_min_idx = 0
        self.last_max_idx = 0
        self.temp_min_idx = 0
        self.temp_max_idx = 0

        self.min_max = []
        self.init_data_and_property()

    @property
    def data(self):
        return self._data

    @property
    def trends(self) -> list:
        return self._trends

    @property
    def up_trends(self) -> list:
        return self._up_trends

    @property
    def down_trends(self) -> list:
        return self._down_trends

    def analysis(self):
        # reference index
        for i in range(1, len(self.data)):
            # 初始化 temp_max_bar, temp_min_bar ....
            self.init_min_max_process(i)

            # 與 last_max_bar, last_min_bar 相比
            self.update_min_max_process(i)

            # 檢查是否發生exception
            self.update_exception(i)

            # save this round status
            self.data["last_min_idx"].iloc[i] = self.last_min_idx
            self.data["last_max_idx"].iloc[i] = self.last_max_idx
            self.data["temp_min_idx"].iloc[i] = self.temp_min_idx
            self.data["temp_max_idx"].iloc[i] = self.temp_max_idx
            print(' check again last_min_idx{}, last_max_idx:{}'.format(
                  self.data.iloc[i, :]['last_min_idx'], self.data.iloc[i, :]['last_max_idx']))

            self._status = np.array(self.directions) * np.array(self._exceptions)
            print('\n\n\n')
        self.existence_min_max_process()
        self.data["min_max"] = self.min_max

    def init_data_and_property(self):
        self.sorted_by_time_series()
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

    def sorted_by_time_series(self):
        self._data = self._data.sort_values(by=['time_series'], ascending=True)
        print("before reset index:\n", self._data.head())
        self._data = self._data.set_index(np.array([i for i in range(len(self._data))]))
        print("before after index:\n", self._data.head())

    def init_trends(self):
        up_trends = Analysor.get_up_trends(self.data.direction.values)
        down_trends = Analysor.get_down_trends(self.data.direction.values)
        trends = Analysor.get_trends(self.data.direction.values)
        self._up_trends = up_trends
        self._down_trends = down_trends
        self._trends = trends

    def get_trend_idx(self, bar_idx):
        for index, trend in enumerate(self.trends):
            if trend[0] <= bar_idx <= trend[1]:
                return index
        return 0

    def init_min_max_process(self, bar_idx):
        trend_idx = self.get_trend_idx(bar_idx)
        directions = self.data.direction.values

        # period of highest high in previous trend when trend status from 1, 0 to -1.
        # 初始得最低點是在一時間內(startBarIndex, endBarIndex)出現最高點
        # self.trends[trend_idx-1][0] 區間的開始
        if directions[bar_idx] == -1 and (directions[bar_idx - 1] == 0 or directions[bar_idx - 1] == 1):
            highest_bar, highest_bar_idx = self.get_highest([0, self.trends[trend_idx][1]])
            self.last_max_idx = highest_bar_idx
            print(" Settle last max is {}(idx: {}) when {}".format(
                self.data.iloc[self.last_max_idx, :]["date"], highest_bar_idx,
                self.data.iloc[bar_idx, :]['date']
            ))
        else:
            print(" Init last max is {} when {}".format(
                self.data.iloc[self.last_max_idx, :]["date"],
                self.data.iloc[bar_idx, :]['date']
            ))

        # period of lowest low in previous trend when trend status from -1,0 to 1.
        # 初始得最低點是在一時間內(startBarIndex, endBarIndex)出現最低點
        # self.trends[trend_idx-1][0] 區間的開始
        print('Index: {}, direction[0]:{}, direction[1]:{}'.format(bar_idx, directions[bar_idx], directions[bar_idx - 1]))
        if directions[bar_idx] == 1 and (directions[bar_idx - 1] == 0 or directions[bar_idx - 1] == -1):
            lowest_bar, lowest_bar_idx = self.get_lowest([0, self.trends[trend_idx][1]])
            self.last_min_idx = lowest_bar_idx
            print(" Settle last min is {}(idx: {}) when {}".format(
                self.data.iloc[self.last_min_idx, :]["date"], lowest_bar_idx,
                self.data.iloc[bar_idx, :]['date']
            ))
        else:
            print(" Init last min is {} when {}".format(
                self.data.iloc[self.last_min_idx, :]["date"],
                self.data.iloc[bar_idx, :]['date']
            ))

    def update_min_max_process(self, bar_idx):
        print(" Update min max process:")
        bar = self.data.iloc[bar_idx, :]
        # previous bar direction is positive
        if self._status[bar_idx - 1] == 1:
            #  current bar high is bigger than temp max high.
            #  (in order to find the max high in this directions)
            if self.data.iloc[self.temp_max_idx]["high"] <= bar["high"]:
                self.temp_max_idx = bar_idx

            # 因為波段到一個段落(由升轉跌)， 將上升波段的出現的最大值更新
            if self._status[bar_idx] == -1:
                # end a period
                self.last_max_idx = self.temp_max_idx
                lowest, self.temp_min_idx = self.get_lowest([self.last_min_idx, bar_idx])

        # previous bar direction is negative
        elif self._status[bar_idx - 1] == -1:
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
              "     last min:{}".format(self._status[bar_idx - 1], self._status[bar_idx - 1],
                                        self.temp_max_idx, self.temp_min_idx,
                                        self.last_max_idx, self.last_min_idx))

    def update_exception(self, bar_idx):
        """
        檢查是否是發生exception situation
        :param bar_idx:
        :return:
        """
        bar = self.data.iloc[bar_idx, :]
        trend_idx = self.get_trend_idx(bar_idx)

        last_min = self.data.low.iloc[self.last_min_idx]
        last_max = self.data.high.iloc[self.last_max_idx]

        temp_max = bar.high
        temp_min = bar.low
        cur_direct = 1 if self.trends[trend_idx] in self._up_trends else -1
        pre_direct = 1 if self.trends[trend_idx - 1] in self._up_trends else -1

        if self._exceptions[bar_idx - 1] == -1:
            #print("     Date(next exception a day):{}".format(row.datetime))
            # exceptional process was already active(如果前一個有Exception的可能, ...)
            if (pre_direct * cur_direct == -1) or \
                    (pre_direct == -1 and last_min >= temp_min) or \
                    (pre_direct == 1 and last_max <= temp_max):
                self._exceptions[bar_idx] = 1
            else:
                self._exceptions[bar_idx] = -1
                print("     following change (dir=1) exception in {}".format(bar.datetime))

        elif pre_direct == cur_direct:
            if cur_direct == 1 and last_min >= temp_min:
                print("     find (dir=1) exception in {}".format(bar.datetime))
                self._exceptions[bar_idx] = -1
            elif cur_direct == -1 and last_max <= temp_max:
                print("     find (dir=-1) exception in {}".format(bar.datetime))
                self._exceptions[bar_idx] = -1
            else:
                self._exceptions[bar_idx] = 1

    def merge_last_min_max(self):
        last_min_unique = self.data.last_min_idx.unique()
        last_max_unique = self.data.last_max_idx.unique()
        merged = np.concatenate((last_min_unique, last_max_unique), axis=0)
        merged = np.unique(merged)
        return sorted(merged)

    def existence_min_max_process(self):
        def get_bar_min_max(bar_idx: int, last_min_max: list):
            for pre_min_max_idx, post_min_max_idx in zip(last_min_max[:-1],
                                                 last_min_max[1:]):
                if pre_min_max_idx <= bar_idx < post_min_max_idx:
                    return post_min_max_idx
            return last_min_max[-1]
        merge_last_min_max = self.merge_last_min_max()
        for idx, row in self.data.iterrows():
            min_max_idx = int(get_bar_min_max(idx, merge_last_min_max))
            col = 'low' if min_max_idx in self.data.last_min_idx.unique() else 'high'
            self.min_max.append(self.data.iloc[min_max_idx, :][col])




if __name__ == '__main__':
    from src.Controller.Process.DataProcessController import DataProcessController
    import os

    path = os.path.join('..', '..', '..', 'data', 'SPY歷史資料2020.csv')
    print(os.path.abspath(path))

    dp_ctl = DataProcessController()
    dp_ctl.process(path, 'csv')

    print("After processing:\n", dp_ctl.data.head())
    aott = AutomaticOneTwoThree(dp_ctl.data,
                                start_date='2020/01/06',
                                end_date='2020/12/31',
                                signal_key='12MA',
                                macd_key='26MA')

    aott.analysis()
    print(aott.data.head())

    print("last min bar (unique)", aott.data.last_min_idx.unique())
    print("last max bar (unique)", aott.data.last_max_idx.unique())

