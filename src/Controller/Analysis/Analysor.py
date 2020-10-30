import abc


class Analysor(metaclass=abc.ABCMeta):
    @staticmethod
    def get_up_trend_index(directions):
        up_trends = []
        start = None
        for i in range(1, len(directions)):
            if directions[i] == 1 and start is None:
                start = i
            if directions[i] == -1 and (directions[i-1] == 1 or directions[i-1] == 0)and start is not None:
                up_trends.append([start, i-1])
                start = None
        if start is not None:
            up_trends.append([start, len(directions)-1])

        return up_trends

    @staticmethod
    def get_down_trends_index(directions):
        down_trends = []
        start = None
        for i in range(1, len(directions)):
            if directions[i] == -1 and start is None:
                start = i
            if directions[i] == 1 and (directions[i-1] == -1 or directions[i - 1] == 0) and start is not None:
                # add up trend to up trends
                down_trends.append([start, i-1])
                # reset variable of up trend
                start = None
        if start is not None:
            down_trends.append([start, len(directions) - 1])

        return down_trends