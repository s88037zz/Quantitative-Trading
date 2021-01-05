from src.Controller.Plot.PlotController import PlotController
from src.Controller.Process.DataProcessController import DataProcessController
from src.Controller.Analysis.AutomaticOneTwoThree import AutomaticOneTwoThree
import unittest, os


class TestPlotController(unittest.TestCase):
    def setUp(self):
        path = os.path.abspath(os.path.join('..', '..', 'data', 'SPY歷史資料2020.csv'))
        self.dp_ctl = DataProcessController()
        self.dp_ctl.process(path, 'csv')
        self.signal_key = '12MA'
        self.macd_key = '26MA'
        self.aott = AutomaticOneTwoThree(self.dp_ctl.data, "2020/01/06", "2020/12/31",
                                         signal_key=self.signal_key, macd_key=self.macd_key)
        self.pc_ctl = PlotController()

    def testCreateFigure(self):
        self.pc_ctl.create_figure(xlabel='Date', ylabel='Price')

    def testShow(self):
        self.pc_ctl.show()

    def testPlotSignalAndMacd(self):
        # plot_prices_trend
        fig, ax = PlotController.create_figure(xlabel='Date', ylabel='Price', title='Signal & MACD')
        self.pc_ctl.plot_prices_trend(self.aott.data, self.signal_key, self.macd_key, ax)
        self.pc_ctl.show()

    def testPlotPriceDirections(self):
        fig, ax = PlotController.create_figure(xlabel='Date', ylabel='Price', title='Signal & MACD Relation')
        self.pc_ctl.plot_prices_trend(self.aott.data, self.signal_key, self.macd_key, ax)
        self.pc_ctl.plot_up_down_trend(self.aott.data, self.signal_key, self.macd_key,
                                      self.aott.up_trends, self.aott.down_trends)
        self.pc_ctl.show()

    def testPlotMinMaxSeparatelyBar(self):
        self.aott.analysis()
        fig, ax = PlotController.create_figure(xlabel='Date', ylabel='Price', title='Signal & MACD Direction')
        self.pc_ctl.plot_last_min_max_bar(self.aott.data, 'last_min_idx', ax)
        self.pc_ctl.plot_last_min_max_bar(self.aott.data, 'last_max_idx', ax)
        self.pc_ctl.show()

    def testIntegratePlot(self):
        self.aott.analysis()
        fig, ax = PlotController.create_figure(xlabel='Date', ylabel='Price', title='Signal & MACD Integration Plot')
        self.pc_ctl.plot_prices_trend(self.aott.data, self.signal_key, self.macd_key, ax)
        self.pc_ctl.plot_prices_bar(self.aott.data, ax)
        self.pc_ctl.plot_last_min_max_bar(self.aott.data, 'last_min_idx', ax)
        self.pc_ctl.plot_last_min_max_bar(self.aott.data, 'last_max_idx', ax)
        self.pc_ctl.show()

    def testPlotOneBar(self):
        test_x = [x for x in range(10)]
        test_open = [value for value in range(50, 60)]
        test_close = [value-3 for value in test_open]
        test_low = [value - 5 for value in test_close]
        test_high = [value + 10 for value in test_open]
        fig, ax = PlotController.create_figure(xlabel='Date', ylabel='Price', title='Plot One Bar Test')
        for x, open, close, high, low in zip(test_x,
                                             test_open, test_close,
                                             test_high, test_low):
            if x % 2 == 0:
                trend = 'up'
            else:
                trend = 'down'
            PlotController.plot_one_bar(x, open, close, high, low, ax, trend)
        self.pc_ctl.show(block=False)
        self.pc_ctl.close(fig)
        try:
            PlotController.plot_one_bar(test_x[0], test_open[0], test_close[0],
                        test_high[0], test_low[0], ax, 'mid')
        except AttributeError as a:
            self.assertTrue(a)

    def testPlotPricesBar(self):
        fig, ax = PlotController.create_figure(size=(15, 12),
                                               xlabel='Date', ylabel='Price', title='Test Plot Prices Bar')
        PlotController.plot_prices_bar(self.aott.data, ax)
        PlotController.show()
