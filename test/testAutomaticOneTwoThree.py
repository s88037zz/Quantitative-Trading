from src.Controller.Analysis.AutomaticOneTwoThree import AutomaticOneTwoThree
from src.Controller.Analysis.DataAnalysisController import DataAnalysisController
from src.Controller.Process.DataProcessController import DataProcessController
import unittest, os


class TestAutomaticOneTwoThree(unittest.TestCase):
    def setUp(self):
        path = os.path.join('.', 'data', 'simple_data.csv')
        self.dp_ctl = DataProcessController()
        self.dp_ctl.process(path, 'csv')
        self.aott = AutomaticOneTwoThree(self.dp_ctl.data, signal='5MA', MACD='12MA')

    def testUpdateDirections(self):
        self.assertFalse('directions' in self.aott.data.columns)
        self.aott.update_directions()
        for d, s, ma in zip(self.aott.data['datetime'],
                            self.aott.data[self.aott.signal],
                            self.aott.data[self.aott.MACD]):
            print(d, s, ma)