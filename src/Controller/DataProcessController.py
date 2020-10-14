import numpy as np
import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import os

class PlotController(object):
    def __init__(self):
        self.data = None

    def load(self, path, type):
        if type == "csv":
            self.data = pd.read_csv(path)
        elif type == "json":
            self.data = pd.read_json(path)
        else:
            raise Exception("Loading process not support {}".format(type))

    def cleanData(self):
        columns_map = {'日期': 'date', '收市': 'close', '開市': 'open', '高': 'high',
                       '低': 'low', '成交量': 'volume', '更改%': 'change'}
        # change columns name:
        self.data = self.data.rename(columns=columns_map)
        print(self.data.columns)

        self.data.change = self.data.change.apply(lambda value: value.replace('%', ''))

    # def getDataSummary(self):

if __name__ == '__main__':
    data_path = os.path.abspath(os.path.join("..", "..", 'data', "SPY歷史資料.csv"))
    print(data_path)
    ctl = PlotController()
    ctl.load(data_path, 'csv')
    ctl.cleanData()