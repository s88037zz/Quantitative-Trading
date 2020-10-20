from src.Controller.TradeGeneratorController import TradeGeneratorController
from src.Controller.DataProcessController import DataProcessController
from datetime import datetime, timedelta
import os, unittest


class TestTradeGeneratorController(unittest.TestCase):

    def setUp(self):
        path = os.path.join('.', 'data', 'simple_data.csv')
        self.tg_ctl = TradeGeneratorController()
        self.da_ctl = DataProcessController()
        self.da_ctl.process(path, 'csv')
        self.date_format = "%Y年%m月%d日"

    def testGeneratelinearPricesRecord(self):
        prices = [300, 540]
        datetimes = [datetime.strptime("2020年10月10日", self.date_format),
                     datetime.strptime("2020年10月11日", self.date_format)]
        new_prices, new_datetimes = self.tg_ctl.generate_linear_prices_record(prices, datetimes, per_hour=2)

        for i in range(1, len(new_prices)):
            self.assertAlmostEqual(20, new_prices[i]-new_prices[i-1], places=3)
            self.assertEqual(timedelta(hours=2), new_datetimes[i] - new_datetimes[i-1])
