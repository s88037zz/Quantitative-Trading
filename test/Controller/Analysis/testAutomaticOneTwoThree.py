from src.Controller.Analysis.AutomaticOneTwoThree import AutomaticOneTwoThree
from src.Controller.Analysis.DataAnalysisController import DataAnalysisController
from src.Controller.Process.DataProcessController import DataProcessController
import unittest, os


class TestAutomaticOneTwoThree(unittest.TestCase):
    def setUp(self):
        path = os.path.join('../..', 'data', 'simple_data.csv')
        self.dp_ctl = DataProcessController()
        self.dp_ctl.process(path, 'csv')
        self.aott = AutomaticOneTwoThree(self.dp_ctl.data, signal='5MA', MACD='12MA')

    def testUpdateDirections(self):
        self.assertFalse('directions' in self.aott.data.columns)
        self.aott.update_directions()
        answer = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0]
        for direct, ans in zip(self.aott.data.directions, answer):
            self.assertEqual(ans, direct)

