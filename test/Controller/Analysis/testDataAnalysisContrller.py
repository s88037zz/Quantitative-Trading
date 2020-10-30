from src.Controller.Analysis.DataAnalysisController import DataAnalysisController
from src.Controller.Process.DataProcessController import DataProcessController
import unittest, os
import numpy as np


class TestDataAnalysisController(unittest.TestCase):
    def setUp(self):
        path = os.path.join('../..', 'data', 'simple_data.csv')
        self.dp_ctl = DataProcessController()
        self.dp_ctl.process(path, 'csv')

        self.da_ctl = DataAnalysisController(self.dp_ctl.data)



