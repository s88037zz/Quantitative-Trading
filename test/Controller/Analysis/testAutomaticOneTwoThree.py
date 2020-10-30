from src.Controller.Analysis.AutomaticOneTwoThree import AutomaticOneTwoThree
from src.Controller.Analysis.DataAnalysisController import DataAnalysisController
from src.Controller.Process.DataProcessController import DataProcessController
from datetime import datetime
import unittest, os
import numpy as np



class TestAutomaticOneTwoThree(unittest.TestCase):
    def setUp(self):
        path = os.path.join('../..', 'data', 'SPY歷史資料after-2010.csv')
        self.dp_ctl = DataProcessController()
        self.dp_ctl.process(path, 'csv')
        self.aott = AutomaticOneTwoThree(self.dp_ctl.data,
                                         start_date='2017/01/01',
                                         end_date='2017/12/31',
                                         signal_key='12MA',
                                         macd_key='26MA')

    def testUpdateDirections(self):
        self.assertFalse('directions' in self.aott.data.columns)
        self.aott.update_directions()
        answer = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0]
        for direct, ans in zip(self.aott.data.directions, answer):
            self.assertEqual(ans, direct)


    def testGetStartDate(self):
        start = self.aott._get_start_datetime(self.dp_ctl.data, "2017/01/01")
        self.assertEqual(np.datetime64(datetime.strptime("2017/01/01", "%Y/%m/%d")), start)

    def testGetEndDate(self):
        end = self.aott._get_end_datetime(self.dp_ctl.data, "2017/12/31")
        self.assertEqual(np.datetime64(datetime.strptime("2017/12/31", "%Y/%m/%d")), end)

    def testUpdateTrends(self):
        trends = self.aott.trends
        self.assertTrue(trends)
        self.assertTrue('up_trend' in trends.keys() and 'down_trend' in trends.keys())
        for key, values in trends.items():
            for value in values:
                # value := trend range(start, end)
                self.assertEqual(2, len(value))
