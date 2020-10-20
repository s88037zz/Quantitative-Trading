from datetime import timedelta

class TradeGeneratorController(object):
    def __init__(self):
        pass

    @staticmethod
    def generate_linear_prices_record(his_prices, datetimes, per_hour=2):
        new_prices = []
        new_datetimes = []
        for i in range(1, len(his_prices)):
            time_delta = timedelta(hours=per_hour)
            prices_delta = (his_prices[i] - his_prices[i-1])*per_hour/24
            for j in range(int(24/per_hour)):
                new_prices.append(his_prices[i-1] + j*prices_delta)
                new_datetimes.append(datetimes[i-1] + j*time_delta)

        return new_prices, new_datetimes

if __name__ == '__main__':
    from src.Controller.DataProcessController import DataProcessController
    import os
    # Inititalize
    path = os.path.abspath(os.path.join("..", "..", 'data', "SPY歷史資料.csv"))
    dp_ctl = DataProcessController()
    dp_ctl.process(path, 'csv')
    prices = dp_ctl.data['close']
    datetimes = dp_ctl.data['datetime']

    tg_ctl = TradeGeneratorController()
    prices, datetimes = tg_ctl.generate_linear_prices_record(prices, datetimes)
    for p, d in zip(prices, datetimes):
        print("{}, {}".format(d, p))