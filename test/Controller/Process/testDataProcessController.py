from src.Controller.Process.DataProcessController import DataProcessController
import unittest, os


class TestDataProcessController(unittest.TestCase):
    def setUp(self):
        self.ctl = DataProcessController()
        self.ctl.load(os.path.join('../..', 'data', 'simple_data.csv'), 'csv')

    def testLoad(self):
        # test load csv data
        test_csv_path = os.path.join('../..', 'data', 'simple_data.csv')
        print("test_csv_path:", test_csv_path)
        self.ctl.load(test_csv_path, 'csv')
        self.assertIsNotNone(self.ctl.data)

        # test load json data
        test_json_path = os.path.join('../..', 'data', 'simple_data.json')
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
        self.assertEqual("2020年7月1日", summary["start_date"])
        self.assertEqual("2020年10月1日", summary['end_date'])

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
        print(self.ctl.data.change[0])

        cols = ["date", "close", "open", "high", "low", "volume", "change"]
        for col, data_col in zip(cols, self.ctl.data.columns):
            self.assertEqual(col, data_col)

        # check type of attri
        self.assertTrue(type(self.ctl.data.close))
        self.assertTrue(type(self.ctl.data.open))
        self.assertTrue(type(self.ctl.data.high))
        self.assertTrue(type(self.ctl.data.low))
        self.assertTrue(type(self.ctl.data.volume))
        self.assertTrue(type(self.ctl.data.change))

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
        self.assertAlmostEqual(332.142, avg_open, places=3)
        self.assertAlmostEqual(333.444, avg_close, places=3)

        # test date is enough to find last 12 days
        avg_open, avg_close = self.ctl.get_avg_by_date(end_date, 12)
        self.assertAlmostEqual(331.4408, avg_open, places=3)
        self.assertAlmostEqual(331.3283, avg_close, places=3)

        # test date is enough to find last 20 days
        avg_open, avg_close = self.ctl.get_avg_by_date(end_date, 20)
        self.assertAlmostEqual(335.4699, avg_open, places=3)
        self.assertAlmostEqual(334.1740, avg_close, places=3)

        # test date is enough to find last 26 days
        avg_open, avg_close = self.ctl.get_avg_by_date(end_date, 26)
        self.assertAlmostEqual(338.7288, avg_open, places=3)
        self.assertAlmostEqual(338.0603, avg_close, places=3)

        # test date is enough to find last 60 days
        avg_open, avg_close = self.ctl.get_avg_by_date(end_date, 60)
        self.assertAlmostEqual(332.9720, avg_open, places=3)
        self.assertAlmostEqual(332.9600, avg_close, places=3)

        # test date isn't enough to find last 10 days
        avg_open, avg_close = self.ctl.get_avg_by_date("2020年9月30日", 10)
        self.assertAlmostEqual(329.8, avg_open, places=3)
        self.assertAlmostEqual(330.008, avg_close, places=3)

    def testProcess(self):
        self.ctl.process(os.path.join('../..', 'data', 'simple_data.csv'), type='csv')
        data = self.ctl.data
        print(data.head())
        self.assertTrue(data.time_series.iloc[0] < data.time_series.iloc[1])
        self.assertTrue(len(self.ctl.ma5) != 0)
        self.assertTrue(len(self.ctl.ma20) != 0)
        self.assertTrue(len(self.ctl.ma60) != 0)
