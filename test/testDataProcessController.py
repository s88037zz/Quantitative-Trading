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

        summary = self.ctl.summary
        self.assertEqual("2020年1月2日", summary["start_date"])
        self.assertEqual("2020年10月9日", summary['end_date'])

    def testAddTimeSeries(self):
        self.ctl.clean_data()
        self.ctl.add_time_series()
        length = None
        length = len(self.ctl.data["time_series"])
        self.assertTrue(length)

    def testAdd5MAAndGet5MA(self):
        self.ctl.clean_data()
        self.ctl.add_time_series()
        self.ctl.add_5MA()

        self.assertTrue(len(self.ctl.ma5) != 0)

    def testAdd20MAAnd20MA(self):
        self.ctl.clean_data()
        self.ctl.add_time_series()
        self.ctl.add_20MA()

        self.assertTrue(len(self.ctl.ma20) != 0)

    def testAdd60And60MA(self):
        self.ctl.clean_data()
        self.ctl.add_time_series()
        self.ctl.add_60MA()

        self.assertTrue(len(self.ctl.ma60) != 0)

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
        summary = self.ctl.summary
        end_date = summary['end_date']

        # test date is enough to find last 10 days
        avg_open, avg_close = self.ctl.get_avg_by_date(end_date, 5)
        self.assertAlmostEqual(340.538, avg_open, places=3)
        self.assertAlmostEqual(341.216, avg_close, places=3)

        # test date is enough to find last 10 days
        avg_open, avg_close = self.ctl.get_avg_by_date(end_date, 20)
        self.assertAlmostEqual(334.5020, avg_open, places=3)
        self.assertAlmostEqual(334.7245, avg_close, places=3)

        # test date is enough to find last 10 days
        avg_open, avg_close = self.ctl.get_avg_by_date(end_date, 60)
        self.assertAlmostEqual(335.085, avg_open, places=3)
        self.assertAlmostEqual(335.1525, avg_close, places=3)

        # test date isn't enough to find last 10 days
        avg_open, avg_close = self.ctl.get_avg_by_date("2020年9月30日", 10)
        self.assertAlmostEqual(329.8, avg_open, places=3)
        self.assertAlmostEqual(330.008, avg_close, places=3)

    def testProcess(self):
        self.ctl.process(os.path.join('.', 'data', 'simple_data.csv'), type='csv')
        data = self.ctl.data
        print(data.head())
        self.assertTrue(data.time_series.iloc[0] < data.time_series.iloc[1])
        self.assertTrue(len(self.ctl.ma5) != 0)
        self.assertTrue(len(self.ctl.ma20) != 0)
        self.assertTrue(len(self.ctl.ma60) != 0)
