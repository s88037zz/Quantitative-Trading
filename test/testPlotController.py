from src.Controller.Plot.PlotController import PlotController
from src.Controller.Process.DataProcessController import DataProcessController
from src.Controller.Analysis.DataAnalysisController import DataAnalysisController
import unittest, os


class TestPlotController(unittest.TestCase):
    def setUp(self):
        path = os.path.join('.', 'data', 'simple_data.csv')
        self.dp_ctl = DataProcessController()
        self.dp_ctl.process(path, 'csv')

        self.pc_ctl = PlotController(self.dp_ctl.data)

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
        # Initialize
        prices = self.dp_ctl.data['close']
        datetimes = self.dp_ctl.data['datetime']

        self.pc_ctl.create_figure(xlabel='Date', ylabel='Price')
        self.pc_ctl.plot_prices(prices, datetimes, 'close')
        self.pc_ctl.plot_MA('5MA')
        self.pc_ctl.plot_MA('12MA')
        self.pc_ctl.plot_MA('26MA')
        self.pc_ctl.plot_MA('60MA')
        self.pc_ctl.show()

