from src.Controller.Analysis.Analysor import Analysor
import unittest


class TestAnalysor(unittest.TestCase):
    def testGetUpTrends(self):
        directions = [-1, 1, 1, 0, 1, 1, 1, 1, 0, -1, 1, -1, 0, 1, 1, 0, 1, 1, 0]
        up_trends = Analysor.get_up_trends(directions)
        answers = [[1, 9], [10, 11], [13, 18]]
        for up_trend, answer in zip(up_trends, answers):
            self.assertEqual(answer[0], up_trend[0])
            self.assertTrue(answer[1], up_trend[1])

    def testGetDownTrends(self):
        directions = [-1, 1, 1, 0, 1, 1, 1, 1, 0, -1, 1, -1, 0, 1, 1, 0, 1, 1, 0]
        down_trends = Analysor.get_down_trends(directions)
        answers = [[0, 1], [9, 10], [11, 13]]
        for up_trend, answer in zip(down_trends, answers):
            self.assertEqual(answer[0], up_trend[0])
            self.assertTrue(answer[1], up_trend[1])

    def testGetTrendInSeq(self):
        directions = [-1, 1, 1, 0, 1, 1, 1, 1, 0, -1, 1, -1, 0, 1, 1, 0, 1, 1, 0]
        trends = Analysor.get_trends(directions)
        answers = [[0, 1], [1, 9], [9, 10], [10, 11], [11, 13], [13, 19]]
        for trend, answer in zip(trends, answers):
            self.assertEqual(answer[0], trend[0])
            self.assertTrue(answer[1], trend[1])