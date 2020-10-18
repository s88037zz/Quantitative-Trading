from src.Controller.PlotController import PlotController
from src.Controller.DataProcessController import DataProcessController
import unittest, os


class TestPlotController(unittest.TestCase):
    def setUp(self):
        path = os.path.join('.', 'data', 'simple_data.csv')
        self.ctl = DataProcessController()
        self.ctl.process(path, 'csv')
        self.pc = PlotController(self.ctl.data)

    def testCreateFigure(self):
        self.pc.create_figure(xlabel='Date', ylabel='Price')

    def testPlotMA(self):
        self.pc.plot_MA('5MA')
        self.pc.plot_MA('20MA')
        self.pc.plot_MA('60MA')

        try:
            self.pc.plot_MA("test")
        except Exception as e:
            self.assertEqual("Plot Controller: plot_MA not support (type: test)", e.args[0])

    def testShow(self):
        self.pc.show()

    def testIntegrativeFunction(self):
        self.pc.create_figure(xlabel='Date', ylabel='Price')
        self.pc.plot_MA('5MA')
        self.pc.plot_MA('20MA')
        self.pc.plot_MA('60MA')
        self.pc.show()

