from src.Controller.Analysis.Analysor import Analysor
import unittest


class TestAnalysor(unittest.TestCase):
    def testGetUpTrends(self):
        directions = [-1, 1, 1, 0, 1, 1, 1, 1, 0, -1, 1, -1, 0, 1, 1, 0, 1, 1, 0]
        up_trends = Analysor.get_up_trend_index(directions)
        answers = [[1, 8], [10, 10], [13, 18]]
        for up_trend, answer in zip(up_trends, answers):
            self.assertEqual(answer[0], up_trend[0])
            self.assertTrue(answer[1], up_trend[1])

    def testGetDownTrends(self):
        directions = [-1, -1, -1, -1, 1, 0, 0, -1, -1, -1, 0, 1, -1, 1]
        down_trends = Analysor.get_down_trends_index(directions)
        print(down_trends)