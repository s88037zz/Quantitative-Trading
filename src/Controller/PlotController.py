from src.Controller.DataAnalysisController import DataAnalysisController
from src.Controller.TradeGeneratorController import TradeGeneratorController
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn, os
import pandas as pd
import seaborn as sb
import numpy as np


class PlotController():
    def __init__(self, data):
        self.data = data
        self.da_ctl = DataAnalysisController(data)
        self.tg_ctl = TradeGeneratorController()

    def create_figure(self, **kwargs):
        plt.figure()
        if 'xlabel' in kwargs.keys():
            plt.xlabel(kwargs['xlabel'])
        if 'ylabel' in kwargs.keys():
            plt.ylabel(kwargs['ylabel'])

    def plot_prices(self, his_prices, datetimes, label=None):
        plt.plot(datetimes, his_prices, label=label)

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

    def plot_relative_of_prices_with_ref(self, his_prices, ref, datetimes,
                                         price_name=None, ref_name=None):
        detail_prices, detail_datetimes = self.tg_ctl.generate_linear_prices_record(his_prices, datetimes)
        detail_ref, detail_datetimes = self.tg_ctl.generate_linear_prices_record(ref, datetimes)
        labels = self.da_ctl.get_relative_of_prices(detail_prices, detail_ref)
        for i in range(1, len(detail_prices)):
            c = 'r' if labels[i-1] == 1 else 'g'
            x = [detail_datetimes[i - 1], detail_datetimes[i]]
            plt.plot(x, [detail_prices[i-1], detail_prices[i]], c=c, label=price_name)
            plt.plot(x, [detail_ref[i-1], detail_ref[i]], c='b', label=ref_name)
        plt.legend(detail_prices, ['price'])

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
    prices = dp_ctl.data['close']
    datetimes = dp_ctl.data['datetime']

    # plot 5MA, 20MA, 60MA
    pc.create_figure(xlabel='Date', ylabel='Price')
    pc.plot_prices(prices, datetimes, label='close')
    # pc.plot_MA("5MA")
    pc.plot_MA("20MA")
    pc.plot_MA("60MA")
    pc.show()

    # plot prices trend
    # trend = da_ctl.get_trend_labels(prices, datetimes)
    # pc.create_figure(xlabel='Date', ylabel='Price')
    # pc.plot_prices_trend(prices, datetimes, trend)
    # pc.show()

