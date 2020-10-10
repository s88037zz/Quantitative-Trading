import numpy as np
import matplotlib.pyplot as plt
import seaborn
import pandas as pd

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