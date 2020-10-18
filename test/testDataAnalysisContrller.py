from src.Controller.DataAnalysisController import DataAnalysisController
from src.Controller.DataProcessController import DataProcessController
import unittest, os


class TestDataAnalysisController(unittest.TestCase):
    def setUp(self):
        path = os.path.join('.', 'data', 'simple_data.csv')
        self.dp_ctl = DataProcessController()
        self.dp_ctl.process(path, 'csv')

        self.da_ctl = DataAnalysisController(self.dp_ctl.data)

    def testGetRaiseAndFallRange(self):
        datetimes = self.dp_ctl.data['datetime']
        prices = self.dp_ctl.data['close']
        raising_ranges = self.da_ctl.get_raising_date_ranges(prices, datetimes)
        raising_range_ans = [[datetimes[1], datetimes[3]], [datetimes[4], datetimes[5]],
        [datetimes[6], datetimes[9]]]

        # test raising range
        for raising_range, ans in zip(raising_ranges, raising_range_ans):
            # 0: start date, 1: end date
            self.assertEqual(ans[0], raising_range[0])
            self.assertEqual(ans[1], raising_range[1])

        # # test falling range
        falling_ranges = self.da_ctl.get_falling_date_ranges(prices, datetimes)
        falling_range_ans = [[datetimes[0], datetimes[1]],
                             [datetimes[3], datetimes[4]],
                             [datetimes[5], datetimes[6]]]
        print(falling_ranges)
        for falling_range, ans in zip(falling_ranges, falling_range_ans):
            #  0: start date, 1: end date
            self.assertEqual(falling_range[0], ans[0])
            self.assertEqual(falling_range[1], ans[1])

