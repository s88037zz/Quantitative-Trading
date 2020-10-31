from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os
import numpy as np


class PlotController():
    def __init__(self):
        pass

    def create_figure(self, **kwargs):
        fig, ax = plt.subplots()
        if 'xlabel' in kwargs.keys():
            plt.xlabel(kwargs['xlabel'])
        if 'ylabel' in kwargs.keys():
            plt.ylabel(kwargs['ylabel'])
        if 'title' in kwargs.keys():
            plt.title(kwargs['title'])
        return fig, ax

    def plot_prices_trend(self, data, signal_key, macd_key, trends):
        signal = data[signal_key]
        macd = data[macd_key]

        fig, ax = self.create_figure(xlabel='Date', ylabel='Price', title='Price Trend')
        x = data["datetime"].apply(lambda x: x.timestamp())
        ax.plot(x, signal, label=signal_key)
        ax.plot(x, macd, label=macd_key)
        print('Up trend:')
        for start_index, end_index in trends["up_trend"]:
            print(' ', start_index, end_index)
            # rectangle = Rectangle((x.values[end_index], signal.iloc[end_index]+1.5),
            #                       timedelta(days=10).total_seconds(),
            #                       3,
            #                       edgecolor='Red',
            #                       fill=False)
            #ax.add_patch(rectangle)
            plt.text(x.values[end_index]-timedelta(days=2).total_seconds(),  signal.iloc[end_index]+3, "H",
                     bbox=dict(facecolor='red', alpha=0.5))

        print('Down trend:')
        for start_index, end_index in trends["down_trend"]:
            print(' ', start_index, end_index)
            plt.text(x.values[end_index]-timedelta(days=2).total_seconds(),  signal.iloc[end_index]-3, "L",
                     bbox=dict(facecolor='green', alpha=0.5, ))

        labels = data['datetime'].apply(lambda x: str(x).split(' ')[0]).values
        plt.xticks(x[::20], labels[::20])
        self.show()

    def show(self):
        plt.xticks(rotation=45)
        plt.legend(loc='best')
        plt.show()


if __name__ == '__main__':
    # Init
    from src.Controller.Process.DataProcessController import DataProcessController
    from src.Controller.Analysis.AutomaticOneTwoThree import AutomaticOneTwoThree
    data_path = os.path.abspath(os.path.join("../..", "..", 'data', "SPY歷史資料after-2010.csv"))
    dp_ctl = DataProcessController()
    dp_ctl.process(data_path, 'csv')
    aott = AutomaticOneTwoThree(dp_ctl.data, '2017/01/01', '2017/12/31')
    pc = PlotController()


    # plot_prices_trend
    pc.plot_prices_trend(aott.data, '12MA', '26MA', aott.trends)

