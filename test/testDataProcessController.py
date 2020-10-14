from src.Controller.DataProcessController import DataProcessController
import unittest, os


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
        test_csv_path = os.path.join('.', 'data', 'simple_data.csv')
        self.ctl.load(test_csv_path)
        summary = self.ctl.getDataSummary()
        self.assertTrue(summary["startData"])
        self.assertTrue(summary['endDate'])

    def testCleanData(self):
        self.ctl.cleanData()
        cols = ["date", "close", "open", "high", "low", "volume", "change"]
        for col, data_col in zip(cols, self.ctl.data.columns):
            self.assertEqual(col, data_col)

        # remove % in change
        self.assertFalse("%" in self.ctl.data.change[0])