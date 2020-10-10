from src.Controller.PlotController import PlotController
import unittest, os


class TestPlotController(unittest.TestCase):
    def setUp(self):
        self.ctl = PlotController()

    def testLoad(self):
        # test load csv data
        test_csv_path = os.path.join('.', 'data', 'simple_data.csv')
        self.ctl.load(test_csv_path, 'csv')
        self.assertIsNotNone(self.ctl.data)

        # test load json data
        self.ctl.data = None
        test_json_path = os.path.join('.', 'data', 'simple_data.json')
        self.ctl.load(test_json_path, 'json')
        self.assertIsNotNone(self.ctl.data)

        # raise exception if type not support
        msg = None
        try:
            self.ctl.load(test_csv_path, "abc")
        except Exception as e:
            msg = e.args[0]
        self.assertEqual(msg, 'Loading process not support abc')




