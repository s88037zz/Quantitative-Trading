from src.Controller.Plot.PlotController import PlotController
from src.Controller.Process.DataProcessController import DataProcessController
from datetime import datetime
import unittest, os
import numpy as np


class TestPlotController(unittest.TestCase):
    def setUp(self):
        path = os.path.join('../..', 'data', 'SPY歷史資料after-2010.csv')
        self.dp_ctl = DataProcessController()
        self.dp_ctl.process(path, 'csv')
        self.pc_ctl = PlotController(self.dp_ctl.data, "2017/01/01", "2017/12/31")

    def testGetStartDate(self):
        start = self.pc_ctl._get_start_datetime(self.dp_ctl.data, "2017/01/01")
        self.assertEqual(np.datetime64(datetime.strptime("2017/01/01", "%Y/%m/%d")), start)

    def testGetEndDate(self):
        end = self.pc_ctl._get_end_datetime(self.dp_ctl.data, "2017/12/31")
        self.assertEqual(np.datetime64(datetime.strptime("2017/12/31", "%Y/%m/%d")), end)

    def testCreateFigure(self):
        self.pc_ctl.create_figure(xlabel='Date', ylabel='Price')

    def testPlotMA(self):
        try:
            self.pc_ctl.plot_MA("test")
        except Exception as e:
            self.assertEqual("Plot Controller: plot_MA not support (type: test)", e.args[0])

        self.pc_ctl.plot_MA('5MA')
        self.pc_ctl.plot_MA('20MA')
        self.pc_ctl.plot_MA('60MA')

    def testShow(self):
        self.pc_ctl.show()

    def testIntegrativeFunction(self):
        self.pc_ctl.create_figure(xlabel='Date', ylabel='Price')
        #self.pc_ctl.plot_prices(prices, datetimes, 'close')
        # self.pc_ctl.plot_MA('5MA')
        self.pc_ctl.plot_MA('12MA')
        self.pc_ctl.plot_MA('26MA')
        # self.pc_ctl.plot_MA('60MA')
        self.pc_ctl.show()

