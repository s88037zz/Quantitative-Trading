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

    def show(self):
        plt.legend()
        plt.show()


if __name__ == '__main__':
    # Init
    from src.Controller.DataProcessController import DataProcessController
    data_path = os.path.abspath(os.path.join("..", "..", 'data', "SPY歷史資料.csv"))
    ctl = DataProcessController()
    ctl.process(data_path, 'csv')
    pc = PlotController(ctl.data)

    pc.create_figure(xlabel='Date', ylabel='Price')
    pc.plot_MA("5MA")
    pc.plot_MA("20MA")
    pc.plot_MA("60MA")
    pc.show()

