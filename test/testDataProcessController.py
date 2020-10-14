from src.Controller.DataProcessController import DataProcessController
from datetime import datetime
import unittest, os, time


class TestPlotController(unittest.TestCase):
    def setUp(self):
        self.ctl = DataProcessController()
        self.ctl.load(os.path.join('.', 'data', 'simple_data.csv'), 'csv')

    def testLoad(self):
        # test load csv data
        test_csv_path = os.path.join('.', 'data', 'simple_data.csv')
        print("test_csv_path:", test_csv_path)
        self.ctl.load(test_csv_path, 'csv')
        self.assertIsNotNone(self.ctl.data)

        # test load json data
        self.ctl.data = None
        test_json_path = os.path.join('.', 'data', 'simple_data.json')
        print("test_json_path:", test_json_path)
        self.ctl.load(test_json_path, 'json')
        self.assertIsNotNone(self.ctl.data)

        # raise exception if type not support
        msg = None
        try:
            self.ctl.load(test_csv_path, "abc")
        except Exception as e:
            msg = e.args[0]
        self.assertEqual(msg, 'Loading process not support abc')
    #

    def testGetDataSummary(self):
        # prepare model
        self.ctl.clean_data()
        self.ctl.add_time_series()

        summary = self.ctl.get_data_summary()
        self.assertEqual(summary["start_date"], "2020年9月28日")
        self.assertEqual(summary['end_date'], "2020年10月9日")
        self.assertEqual(summary['last7_avg'], )
        self.assertEqual(summary['last30_avg'], )
        self.assertEqual(summary['last90_avg'], )

    def testAddTimeSeries(self):
        self.ctl.clean_data()
        self.ctl.add_time_series()
        length = None
        length = len(self.ctl.data["time_series"])
        self.assertTrue(length)

    def testCleanData(self):
        bef_row, bef_col = self.ctl.data.shape
        self.ctl.clean_data()
        aft_row, aft_col = self.ctl.data.shape
        print(bef_row, bef_col, aft_row, aft_col)

        cols = ["date", "close", "open", "high", "low", "volume", "change"]
        for col, data_col in zip(cols, self.ctl.data.columns):
            self.assertEqual(col, data_col)

        # remove % in change
        self.assertFalse("%" in self.ctl.data.change[0])

        # check quantity of data after clean data is smaller than before.
        self.assertTrue(aft_row < bef_row)

    def testGetAverageFromDate(self):
        # prepare model
        self.ctl.clean_data()
        self.ctl.add_time_series()
        summary = self.ctl.get_data_summary()
        start = datetime.strptime(summary['start_date'], '%Y年%m月%d日')
        end = datetime.strptime(summary['end_date'], '%Y年%m月%d日')

        # test
        avg_open, avg_close = self.ctl.get_avg_by_date(start, end)
        self.assertEqual(avg_open, 336.635)
        self.assertEqual(avg_close, 337.17125)