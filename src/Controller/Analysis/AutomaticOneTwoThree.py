

class AutomaticOneTwoThree(object):
    def __init__(self, data, signal='12MA', MACD="26MA"):
        self._data = data.copy()
        self.signal = signal
        self.MACD = MACD

    @property
    def data(self):
        return  self._data

    def analysis(self):
        pass

    def update_directions(self):
        if self.signal not in self.data.columns or self.MACD not in self.data.columns:
            raise Exception("AutomaticOneTwoThree pars error!(signal or macd is not in Dataframe columns.)")
        fast_line = self._data[self.signal]
        slow_line = self._data[self.MACD]
        directions = []
        for f, s in zip(fast_line, slow_line):
            if f > s:
                directions.append(1)
            elif f == s:
                directions.append(0)
            else:
                directions.append(-1)

        self._data['directions'] = directions

