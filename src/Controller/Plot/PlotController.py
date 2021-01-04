from datetime import timedelta
from pandas import DataFrame
import matplotlib.pyplot as plt
import os


class PlotController:
    def __init__(self):
        pass

    @staticmethod
    def create_figure(**kwargs):
        fig, ax = plt.subplots()
        if 'xlabel' in kwargs.keys():
            plt.xlabel(kwargs['xlabel'])
        if 'ylabel' in kwargs.keys():
            plt.ylabel(kwargs['ylabel'])
        if 'title' in kwargs.keys():
            plt.title(kwargs['title'])
        return fig, ax

    @staticmethod
    def plot_prices_trend(data: DataFrame, signal_key: str, macd_key: str, ax):
        signal = data[signal_key]
        macd = data[macd_key]

        x = data["datetime"]
        ax.plot(x, signal, label=signal_key)
        ax.plot(x, macd, label=macd_key)

    @staticmethod
    def plot_up_down_trend(data: DataFrame, signal_key: str, macd_key: str,
                           up_trends: list, down_trends: list):
        signal = data[signal_key]
        macd = data[macd_key]
        print('Up trend:')

        x = data["datetime"]
        for trend in up_trends:
            start_index, end_index = trend[0], trend[1]
            print(' start:{}, end:{} '.format(data["datetime"].iloc[start_index],
                                              data["datetime"].iloc[end_index-1]))

            plt.text(x.values[end_index-1]-timedelta(days=2).total_seconds(),  signal.iloc[end_index-1]+5, "H",
                     bbox=dict(facecolor='red', alpha=0.5))

        print('Down trend:')
        for trend in down_trends:
            start_index, end_index = trend[0], trend[1]
            print(' start:{}, end:{} '.format(data["datetime"].iloc[start_index],
                                              data["datetime"].iloc[end_index-1]))
            plt.text(x.values[end_index-1]-timedelta(days=2).total_seconds(),  signal.iloc[end_index-1]-5, "L",
                     bbox=dict(facecolor='green', alpha=0.5))

    @staticmethod
    def plot_last_min_max_bar(data: DataFrame, last_series_type: str, ax):
        if last_series_type == 'last_min_idx':
            color = 'g'
            price = 'low'
        elif last_series_type == 'last_max_idx':
            color = 'r'
            price = 'high'
        else:
            raise ValueError("last_series_type need to be 'last_min_idx' or 'last_max_idx'!")

        x = data["datetime"]
        y = data[last_series_type].apply(lambda idx: data.iloc[int(idx), :][price])
        ax.plot(x, y, color=color)

    @staticmethod
    def plot_one_bar(x, open, close, high, low, ax, trend):
        if trend == 'up':
            color = 'r'
        elif trend == 'down':
            color = 'g'
        else:
            raise ValueError('type only accept "up" or "down"!')
        upper, lower = (open, close) if open >= close else (close, open)

        ax.plot([x, x], [open, close], color=color, linewidth=2)

        ax.plot([x, x], [upper, high], color='k', linewidth=0.5)
        ax.plot([x, x], [lower, low], color='k', linewidth=0.5)


    @staticmethod
    def show(block=True):
        plt.xticks(rotation=45)
        plt.legend(loc='best')
        plt.show(block=block)

    @staticmethod
    def close(fig=None):
        plt.close(fig=fig)

if __name__ == '__main__':
    # Init
    from src.Controller.Process.DataProcessController import DataProcessController
    from src.Controller.Analysis.AutomaticOneTwoThree import AutomaticOneTwoThree
    data_path = os.path.abspath(os.path.join("../..", "..", 'data', "SPY歷史資料after-2010.csv"))
    dp_ctl = DataProcessController()
    dp_ctl.process(data_path, 'csv')
    aott = AutomaticOneTwoThree(dp_ctl.data, '2017/01/01', '2017/12/31', signal_key='1MA')
    pc = PlotController()

