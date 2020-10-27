import matplotlib.pyplot as plt
import os
import numpy as np


class PlotController():
    def __init__(self, data):
        self.data = data

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

