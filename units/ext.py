from .units import *


class SmallDistance(Distance):

    @staticmethod
    def accuracy(units: Unit):
        return Distance.accuracy(units) + 2


class BigDistance(Distance):

    @staticmethod
    def accuracy(units: Unit):
        accuracy = Distance.accuracy(units)

        if accuracy <= 2:
            return 0
        return Distance.accuracy(units) - 2
