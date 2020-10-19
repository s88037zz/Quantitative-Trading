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

    def testGetRaiseAndFallRange(self):
        datetimes = self.dp_ctl.data['datetime']
        prices = self.dp_ctl.data['close']
        raising_ranges = self.da_ctl.get_raising_date(prices, datetimes)
        raising_range_ans = [[datetimes[1], datetimes[3]], [datetimes[4], datetimes[5]],
        [datetimes[6], datetimes[9]]]

        # test raising range
        for raising_range, ans in zip(raising_ranges, raising_range_ans):
            # 0: start date, 1: end date
            self.assertEqual(ans[0], raising_range[0])
            self.assertEqual(ans[1], raising_range[1])

        # # test falling range
        falling_ranges = self.da_ctl.get_falling_date(prices, datetimes)
        falling_range_ans = [[datetimes[0], datetimes[1]],
                             [datetimes[3], datetimes[4]],
                             [datetimes[5], datetimes[6]]]

        for falling_range, ans in zip(falling_ranges, falling_range_ans):
            #  0: start date, 1: end date
            self.assertEqual(falling_range[0], ans[0])
            self.assertEqual(falling_range[1], ans[1])

    def testGetRaisingLabels(self):
        datetimes = self.dp_ctl.data['datetime']
        prices = self.dp_ctl.data['close']
        raising_trend = self.da_ctl.get_raising_labels(prices, datetimes)
        self.assertEqual(9,  np.count_nonzero(raising_trend == 1))

    def testGetFallingLabels(self):
        datetimes = self.dp_ctl.data['datetime']
        prices = self.dp_ctl.data['close']
        falling_trend = self.da_ctl.get_falling_labels(prices, datetimes)
        print(falling_trend)
        self.assertEqual(6, np.count_nonzero(falling_trend == -1))

    def testGetTrendLabels(self):
        datetimes = self.dp_ctl.data['datetime']
        prices = self.dp_ctl.data['close']
        trend = self.da_ctl.get_falling_labels(prices, datetimes)
        self.assertEqual(9, np.count_nonzero(trend == 1))
        self.assertEqual(6, np.count_nonzero(trend == -1))
