from src.Controller.PlotController import PlotController
from src.Controller.DataProcessController import DataProcessController
from src.Controller.DataAnalysisController import DataAnalysisController
import unittest, os


class TestPlotController(unittest.TestCase):
    def setUp(self):
        path = os.path.join('.', 'data', 'simple_data.csv')
        self.dp_ctl = DataProcessController()
        self.dp_ctl.process(path, 'csv')

        self.pc_ctl = PlotController(self.dp_ctl.data)
        self.da_ctl = DataAnalysisController(self.dp_ctl.data)

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

    def testPlotPricesTrend(self):
        prices = self.da_ctl.data['close']
        datetimes = self.da_ctl.data['datetime']
        trend = self.da_ctl.get_trend_labels(prices, datetimes)

        self.pc_ctl.plot_prices_trend(prices, datetimes, trend)

    def testPlotRelativeOfPrices(self):
        prices = self.dp_ctl.data['close']
        ma5 = self.dp_ctl.data['5MA']
        datetimes = self.dp_ctl.data['datetimes']
        self.pc_ctl.plot_relative_of_prices_with_ref(prices, ma5, datetimes)

    def testIntegrativeFunction(self):
        # Initialize
        prices = self.dp_ctl.data['close']
        ma5 = self.dp_ctl.data['5MA']
        datetimes = self.dp_ctl.data['datetime']

        # self.pc_ctl.create_figure(xlabel='Date', ylabel='Price')
        # self.pc_ctl.plot_prices(prices, datetimes, 'close')
        # self.pc_ctl.plot_MA('5MA')
        # self.pc_ctl.plot_MA('20MA')
        # self.pc_ctl.plot_MA('60MA')
        # self.pc_ctl.show()

        # self.pc_ctl.create_figure(xlabel="Date", ylabel='Price')
        # trend_labels = self.da_ctl.get_trend_labels(prices, datetimes)
        # self.pc_ctl.plot_prices_trend(prices, datetimes, trend_labels)
        # self.pc_ctl.show()

        # self.pc_ctl.create_figure(xlabel="Date", ylabel='Price')
        # self.pc_ctl.plot_prices_with_ref(prices, datetimes, ma5)
        # self.pc_ctl.show()

        self.pc_ctl.create_figure(xlabel="Date", ylabel='Price')
        self.pc_ctl.plot_relative_of_prices_with_ref(prices, ma5, datetimes)
        self.pc_ctl.show()