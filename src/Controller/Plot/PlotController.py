from datetime import datetime
import matplotlib.pyplot as plt
import os
import numpy as np


class PlotController():
    def __init__(self, data, start_date=None, end_date=None):
        self.start_datetime = self._get_start_datetime(data, start_date)
        self.end_datetime = self._get_end_datetime(data, end_date)
        self.data = self._get_data_in_time(data)
        print(self.data.shape
              )
    def _get_data_in_time(self, data):
        return data.loc[(self.start_datetime <= data.datetime) & (data.datetime <= self.end_datetime)]

    def _get_start_datetime(self, data, start_date=None):
        if start_date is None:
            return data.datetime.values[0]
        elif data.datetime.values[0] <= np.datetime64(datetime.strptime(start_date, "%Y/%m/%d"))\
                <= data.datetime.values[-1]:
            return np.datetime64(datetime.strptime(start_date, "%Y/%m/%d"))
        else:
            raise Exception("The start datetime isn't in data")

    def _get_end_datetime(self, data, end_date=None):
        if end_date is None:
            return data.datetime.values[-1]
        elif data.datetime.values[0] <= np.datetime64(datetime.strptime(end_date, "%Y/%m/%d")) \
                <= data.datetime.values[-1]:
            return np.datetime64(datetime.strptime(end_date, "%Y/%m/%d"))
        else:
            raise Exception("The end datetime isn't in data")

    def create_figure(self, **kwargs):
        plt.figure()
        if 'xlabel' in kwargs.keys():
            plt.xlabel(kwargs['xlabel'])
        if 'ylabel' in kwargs.keys():
            plt.ylabel(kwargs['ylabel'])
        if 'title' in kwargs.keys():
            plt.title(kwargs['title'])

    def plot_prices(self, his_prices, datetimes, label=None):
        plt.plot(datetimes, his_prices, label=label)

    def plot_MA(self, type):
        if "MA" in type and type in self.data.columns:
            plt.plot(self.data.datetime, self.data[type], label=type)
        else:
            raise Exception("Plot Controller: plot_MA not support (type: {})".format(type))

    def show(self):
        plt.xticks(rotation=45)
        plt.legend(loc='best')
        plt.show()


if __name__ == '__main__':
    # Init
    from src.Controller.Process.DataProcessController import DataProcessController
    from src.Controller.Analysis.DataAnalysisController import DataAnalysisController
    data_path = os.path.abspath(os.path.join("../..", "..", 'data', "SPY歷史資料 (3 months).csv"))
    dp_ctl = DataProcessController()
    dp_ctl.process(data_path, 'csv')
    da_ctl = DataAnalysisController(dp_ctl.data)
    pc = PlotController(dp_ctl.data)
    prices = dp_ctl.data['close']
    datetimes = dp_ctl.data['datetime']

    # plot 5MA, 20MA, 60MA
    pc.create_figure(xlabel='Date', ylabel='Price')
    pc.plot_prices(prices, datetimes, label='close')
    pc.plot_MA("5MA")
    pc.plot_MA("20MA")
    pc.plot_MA("60MA")
    pc.show()

