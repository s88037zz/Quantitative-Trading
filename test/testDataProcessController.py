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

    def testAddTimeSeries(self):
        self.ctl.clean_data()
        self.ctl.add_time_series()
        length = None
        length = len(self.ctl.data["time_series"])
        self.assertTrue(length)

    def testAdd5MA(self):
        self.ctl.clean_data()
        self.ctl.add_time_series()
        self.ctl.add_5MA()

        self.assertTrue(len(self.ctl.data["5MA"]) != 0)

    def testAdd20MA(self):
        self.ctl.clean_data()
        self.ctl.add_time_series()
        self.ctl.add_20MA()

        self.assertTrue(len(self.ctl.data["20MA"]) != 0)

    def testAdd60(self):
        self.ctl.clean_data()
        self.ctl.add_time_series()
        self.ctl.add_60MA()

        self.assertTrue(len(self.ctl.data["60MA"]) != 0)

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

    def testGetAverageByDate(self):
        # prepare model
        self.ctl.clean_data()
        self.ctl.add_time_series()
        summary = self.ctl.get_data_summary()
        start = summary['start_date']

        # test date is enough to find last 10 days
        avg_open, avg_close = self.ctl.get_avg_by_date(start, 10)
        self.assertEqual(333.38, avg_open)
        self.assertEqual(334.19, avg_close)
        # test date isn't enough to find last 10 days

        avg_open, avg_close = self.ctl.get_avg_by_date("2020年9月30日", 10)
        self.assertAlmostEqual(333.4833, avg_open, places=3)
        self.assertAlmostEqual(333.8166, avg_close, places=3)
