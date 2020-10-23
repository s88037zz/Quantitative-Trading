from src.Controller.DataAnalysisController import DataAnalysisController
from src.Controller.DataProcessController import DataProcessController
import unittest, os
import numpy as np

class TestDataAnalysisController(unittest.TestCase):
    def setUp(self):
        path = os.path.join('.', 'data', 'simple_data.csv')
        self.dp_ctl = DataProcessController()
        self.dp_ctl.process(path, 'csv')

        self.da_ctl = DataAnalysisController(self.dp_ctl.data)

    def testGetRaisingLabels(self):
        datetimes = self.dp_ctl.data['datetime']
        prices = self.dp_ctl.data['close']
        raising_trend = self.da_ctl.get_raising_labels(prices, datetimes)
        self.assertEqual(42,  np.count_nonzero(raising_trend == 1))

    def testGetFallingLabels(self):
        datetimes = self.dp_ctl.data['datetime']
        prices = self.dp_ctl.data['close']
        falling_trend = self.da_ctl.get_falling_labels(prices, datetimes)
        print(falling_trend)
        self.assertEqual(22, np.count_nonzero(falling_trend == -1))

    def testGetTrendLabels(self):
        datetimes = self.dp_ctl.data['datetime']
        prices = self.dp_ctl.data['close']
        trend = self.da_ctl.get_trend_labels(prices, datetimes)
        self.assertEqual(6, np.count_nonzero(trend == 1))
        self.assertEqual(3, np.count_nonzero(trend == -1))

    def testGetRelativeOfPrices(self):
        prices = [100, 50, 10, 5, 10]
        ma5 = [200, 100, 5, 1, 0]
        relative = self.da_ctl.get_relative_of_prices(prices, ma5)
        print(relative)
        ans = [-1, -1, 1, 1, 1]
        for r, a in zip(relative, ans):
            self.assertEqual(r, a)

