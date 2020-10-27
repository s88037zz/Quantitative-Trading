from src.Controller.Process.DataProcessController import DataProcessController
from src.Controller.Analysis.DataAnalysisController import DataAnalysisController
from src.Controller.Plot.PlotController import PlotController
import os


class Controller(object):
    def __init__(self):
        data_path = os.path.abspath(os.path.join("..", "..", 'data', "SPY歷史資料.csv"))
        self.dp_ctl = DataProcessController()
        self.dp_ctl.process(data_path, 'csv')
        self.p_ctl = PlotController(self.dp_ctl.data)
        self.da_ctl = DataAnalysisController(self.dp_ctl.data)
        self.records = []

if __name__  == '__main__':
    ctl = Controller()
