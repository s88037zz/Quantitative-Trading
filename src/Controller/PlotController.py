import matplotlib.pyplot as plt
import seaborn, os
import pandas as pd
import seaborn as sb
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

    def plot_MA(self, type):
        if type == "5MA" or type == "20MA" or type == '60MA':
            plt.plot(self.data.datetime, self.data[type], label=type)
        else:
            raise Exception("Plot Controller: plot_MA not support (type: {})".format(type))

    def plot_prices_trend(self, his_prices, datetimes, trend):
        color = ['r' if x==1 else 'g' for x in trend]
        for i in range(1, len(his_prices)):
            x = [datetimes[i-1], datetimes[i]]
            y = [his_prices[i-1], his_prices[i]]
            c = color[i-1]
            plt.plot(x, y, c=c)
        plt.title("Price Trend")

    def show(self):
        plt.xticks(rotation=45)
        plt.legend(loc='best')
        plt.show()


if __name__ == '__main__':
    # Init
    from src.Controller.DataProcessController import DataProcessController
    from src.Controller.DataAnalysisController import DataAnalysisController
    data_path = os.path.abspath(os.path.join("..", "..", 'data', "SPY歷史資料.csv"))
    dp_ctl = DataProcessController()
    dp_ctl.process(data_path, 'csv')
    da_ctl = DataAnalysisController(dp_ctl.data)
    pc = PlotController(dp_ctl.data)

    # plot 5MA, 20MA, 60MA
    # pc.create_figure(xlabel='Date', ylabel='Price')
    # pc.plot_MA("5MA")
    # pc.plot_MA("20MA")
    # pc.plot_MA("60MA")
    # pc.show()

    # plot prices trend
    prices = dp_ctl.data['close']
    datetimes = dp_ctl.data['datetime']
    trend = da_ctl.get_trend_labels(prices, datetimes)
    pc.create_figure(xlabel='Date', ylabel='Price')
    pc.plot_prices_trend(prices, datetimes, trend)
    pc.show()

