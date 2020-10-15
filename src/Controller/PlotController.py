import matplotlib.pyplot as plt
import seaborn, os
import pandas as pd
import seaborn as sb
import numpy as np


class PlotController():
    def __init__(self, data):
        self.data = data

    def create_figure(self):
        plt.figure()

    def plot_MA(self, type):
        if type == "5MA" or type == "20MA" or type == '60MA':
            plt.plot(self.data.time_series, self.data[type])
        else:
            raise  Exception("Plot Controller: plot_MA not support (type: {})".format(type))

    def show(self):
        plt.show()


if __name__ == '__main__':
    # Init
    from src.Controller.DataProcessController import DataProcessController
    data_path = os.path.abspath(os.path.join("..", "..", 'data', "SPY歷史資料.csv"))
    ctl = DataProcessController()
    ctl.load(data_path, 'csv')
    pc = PlotController(ctl.data)

