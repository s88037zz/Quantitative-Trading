from src.Controller.Analysis.AutomaticOneTwoThree import AutomaticOneTwoThree
from src.Controller.Plot.PlotController import PlotController
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

    def testInitDirections(self):
        self.assertFalse('directions' in self.aott.data.columns)
        self.aott.init_directions()
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

    def testeInitTrendsAndGetTrendIndex(self):
        trends = self.aott.trends
        trend_idx = self.aott.get_trend_idx(30)
        self.assertTrue(trend_idx == 0)
        trend_idx = self.aott.get_trend_idx(40)
        self.assertTrue(trend_idx == 1)
        trend_idx = self.aott.get_trend_idx(250)
        self.assertTrue(trend_idx == 6)

    def testInitMinMaxProcess(self):
        self.aott.init_min_max_process(0)
        self.assertTrue(self.aott.last_min_idx == 0)
        self.aott.init_min_max_process(53)
        self.assertTrue(self.aott.last_max_idx == 39)
        self.aott.init_min_max_process(111)
        self.assertTrue(self.aott.last_max_idx == 109)
        self.aott.init_min_max_process(148)
        self.assertTrue(self.aott.last_max_idx == 142)

    def testUpdateException(self):
        self.aott.update_exception()
        exceptions = self.aott._exceptions
        directions = self.aott.data.directions.values
        for i, (e, d) in enumerate(zip(exceptions, directions)):
            print(self.aott.data.date.values[i], d, e)

        idx = np.where(self.aott.data.date == "2017年10月20日")[0]
        self.assertEqual(1.0, directions[idx][0] * exceptions[idx][0])
        idx = np.where(self.aott.data.date == "2017年5月17日")[0]
        self.assertEqual(1.0, self.aott.data.directions.iloc[idx].values[0] * exceptions[idx])
        idx = np.where(self.aott.data.date == "2017年5月17日")[0]

