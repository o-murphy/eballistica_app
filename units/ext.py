from .units import *


class SmallDistance(Distance):

    @staticmethod
    def accuracy(units: Unit):
        return Distance.accuracy(units) + 2
