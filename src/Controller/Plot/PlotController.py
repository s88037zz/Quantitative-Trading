from datetime import timedelta
from pandas import DataFrame
import matplotlib.pyplot as plt
import os


class PlotController:
    def __init__(self):
        pass

    @staticmethod
    def create_figure(**kwargs):
        if 'size' in kwargs.keys():
            fig, ax = plt.subplots(size=kwargs['size'])
        else:
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

        x = data["datetime"].apply(lambda date: date.strftime("%Y/%m/%d"))
        ax.plot(x, signal, label=signal_key)
        ax.plot(x, macd, label=macd_key)

    @staticmethod
    def plot_min_max(data: DataFrame, ax):
        x = data["datetime"].apply(lambda date: date.strftime("%Y/%m/%d"))
        y = data["min_max"]
        ax.plot(x, y, label="min max value")

    @staticmethod
    def plot_up_down_trend(data: DataFrame, signal_key: str, macd_key: str,
                           up_trends: list, down_trends: list):
        signal = data[signal_key]
        macd = data[macd_key]
        print('Up trend:')

        x = data["datetime"]
        for trend in up_trends:
            start_idx, end_idx = trend[0], trend[1]
            plot_idx = (start_idx + end_idx) // 2

            plt.text(x.values[plot_idx],  signal.iloc[plot_idx]+5, "H",
                     bbox=dict(facecolor='red', alpha=0.5))

        print('Down trend:')
        for trend in down_trends:
            start_idx, end_idx = trend[0], trend[1]
            plot_idx = (start_idx + end_idx) // 2

            plt.text(x.values[plot_idx],  signal.iloc[plot_idx]-5, "L",
                     bbox=dict(facecolor='green', alpha=0.5))

    @staticmethod
    def plot_last_min_max_bar(data: DataFrame, last_series_type: str, ax):
        if last_series_type == 'last_min_idx':
            color = 'g'
            price = 'low'
            label = 'last min price'
        elif last_series_type == 'last_max_idx':
            color = 'r'
            price = 'high'
            label = 'last max price'
        else:
            raise ValueError("last_series_type need to be 'last_min_idx' or 'last_max_idx'!")

        x = data["datetime"].apply(lambda datetime: datetime.strftime('%Y/%m/%d'))
        y = data[last_series_type].apply(lambda idx: data.iloc[int(idx), :][price])
        ax.plot(x, y, color=color, label=label)
        PlotController.set_xticks(data, ax)

    @staticmethod
    def plot_one_bar(x, open, close, high, low, ax, trend):
        if trend == 'up':
            color = 'r'
        elif trend == 'down':
            color = 'g'
        else:
            raise AttributeError('type only accept "up" or "down"!')
        upper, lower = (open, close) if open >= close else (close, open)

        ax.plot([x, x], [open, close], color=color, linewidth=2)

        ax.plot([x, x], [upper, high], color='k', linewidth=0.5)
        ax.plot([x, x], [lower, low], color='k', linewidth=0.5)

    @staticmethod
    def plot_prices_bar(data: DataFrame, ax):
        for bar_idx, row in data.iterrows():
            x = row['datetime'].strftime('%Y/%m/%d')
            open = row['open']
            close = row['close']
            high = row['high']
            low = row['low']
            trend = 'down' if open >= close else 'up'
            PlotController.plot_one_bar(x, open, close, high, low, ax, trend)
        PlotController.set_xticks(data, ax)

    @staticmethod
    def set_xticks(data, ax, interval=20):
        xlabels = data["datetime"][::interval].apply(lambda date: date.strftime("%Y/%m/%d"))
        ax.set_xticks(range(0, len(data), interval))
        ax.set_xticklabels(list(xlabels))

    @staticmethod
    def show(block=True, rotation=90):
        plt.xticks(rotation=rotation)
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

