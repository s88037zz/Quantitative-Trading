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

    def testeInitTrends(self):
        trends = self.aott.trends
        self.assertTrue(trends)
        self.assertTrue('up_trend' in trends.keys() and 'down_trend' in trends.keys())
        for key, values in trends.items():
            for value in values:
                # value := trend range(start, end)
                self.assertEqual(2, len(value))

    def testFindHighestInTrend(self):
        trend = [0, 4]
        value, index = self.aott.find_highest(trend)
        self.assertAlmostEqual(227.75, value, places=3)
        self.assertEqual(3, index)

    def testFindLowestInTrend(self):
        trend = [0, 4]
        value, index = self.aott.find_lowest(trend)
        self.assertAlmostEqual(223.880, value, places=3)
        self.assertEqual(0, index)

    def testInitMinMaxProcess(self):
        self.aott.init_min_max_process()
        # print(self.aott.data['last_min_idx'].values)
        # print(self.aott.data['last_max_idx'].values)

        for ans, idx in zip(np.array([0, 57, 123]), self.aott.data['last_min_idx'].unique()):
            self.assertEqual(ans, idx)
        for ans, idx in zip(np.array([0, 39, 109, 142]), self.aott.data['last_max_idx'].unique()):
            self.assertEqual(ans, idx)


    def testUpdateExecepetion(self):
        self.aott.update_exceptions()
        exceptions = self.aott._exceptions
        directions = self.aott.data.directions.values
        for i, (e, d) in enumerate(zip(exceptions, directions)):
            print(self.aott.data.date.values[i], d, e)

        idx = np.where(self.aott.data.date == "2017年10月20日")[0]
        self.assertEqual(1.0, directions[idx][0] * exceptions[idx][0])
        idx = np.where(self.aott.data.date == "2017年5月17日")[0]
        self.assertEqual(1.0, self.aott.data.directions.iloc[idx].values[0] * exceptions[idx])
        idx = np.where(self.aott.data.date == "2017年5月17日")[0]



"""
In a Trend, there contain:
highest, highest_index
lowest, lowest_index
Exception[t_index] 
Status[t_index]
Direction[t_index]
"""