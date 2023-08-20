import enum


class TwistDir(enum.IntEnum):
    Right = 0
    Left = 1


class DragModel(enum.IntEnum):
    G1 = 0
    G7 = 1
    CDM = -1
