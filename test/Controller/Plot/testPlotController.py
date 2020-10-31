from src.Controller.Plot.PlotController import PlotController
from src.Controller.Process.DataProcessController import DataProcessController
from src.Controller.Analysis.AutomaticOneTwoThree import AutomaticOneTwoThree
from datetime import datetime
import unittest, os
import numpy as np


class TestPlotController(unittest.TestCase):
    def setUp(self):
        path = os.path.join('..', '..', 'data', 'SPY歷史資料after-2010.csv')
        self.dp_ctl = DataProcessController()
        self.dp_ctl.process(path, 'csv')
        self.aott = AutomaticOneTwoThree(self.dp_ctl.data, "2017/01/01", "2017/12/31")
        self.pc_ctl = PlotController()

    def testCreateFigure(self):
        self.pc_ctl.create_figure(xlabel='Date', ylabel='Price')

    def testShow(self):
        self.pc_ctl.show()

    def testPlotPriceTrend(self):
        # plot_prices_trend
        self.pc_ctl.plot_prices_trend(self.aott.data, '12MA', '26MA', self.aott.trends)