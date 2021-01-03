from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
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

        fig, ax = pc.create_figure(xlabel='Date', ylabel='Price', title='Init Min Max process')
        x = data["datetime"].apply(lambda x: x.timestamp())
        ax.plot(x, signal, label=signal_key)
        ax.plot(x, macd, label=macd_key)
        print('Up trend:')
        for start_index, end_index in trends["up_trends"]:
            print(' ', start_index, end_index)

            plt.text(x.values[end_index-1]-timedelta(days=2).total_seconds(),  signal.iloc[end_index-1]+5, "H",
                     bbox=dict(facecolor='red', alpha=0.5))

        print('Down trend:')
        for start_index, end_index in trends["down_trends"]:
            print(' ', start_index, end_index)
            plt.text(x.values[end_index-1]-timedelta(days=2).total_seconds(),  signal.iloc[end_index-1]-5, "L",
                     bbox=dict(facecolor='green', alpha=0.5))

        pc.plot_last_min_max_bar(aott.data, '1MA', "last_min_idx", ax)
        pc.plot_last_min_max_bar(aott.data, '1MA', "last_max_idx", ax)
        labels = data['datetime'].apply(lambda x: str(x).split(' ')[0]).values
        plt.xticks(x[::20], labels[::20])
        self.show()

    def plot_last_min_max_bar(self, data, signal_key, last_series_type, ax):
        color = 'r' if last_series_type == 'last_max_idx' else 'g'
        print(last_series_type+":")
        for last_idx in data[last_series_type].unique():
            x = data["datetime"].iloc[last_idx].timestamp()
            ax.plot([x, x], [data.high.iloc[last_idx], data.low.iloc[last_idx]], color=color)


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
    aott = AutomaticOneTwoThree(dp_ctl.data, '2017/01/01', '2017/12/31', signal_key='1MA')
    pc = PlotController()


    # plot_prices_trend
    pc.plot_prices_trend(aott.data, '1MA', '26MA', {"up_trends": aott.up_trends,
                                                     "down_trends": aott.down_trends})

    pc.show()
