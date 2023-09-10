from abc import ABC
from enum import IntEnum
from math import pi, atan, tan


class Unit(IntEnum):
    Radian = 0
    Degree = 1
    MOA = 2
    Mil = 3
    MRad = 4
    Thousand = 5
    InchesPer100Yd = 6
    CmPer100M = 7

    Inch = 10
    Foot = 11
    Yard = 12
    Mile = 13
    NauticalMile = 14
    Millimeter = 15
    Centimeter = 16
    Meter = 17
    Kilometer = 18
    Line = 19

    FootPound: int = 30
    Joule: int = 31

    MmHg = 40
    InHg = 41
    Bar = 42
    HP = 43
    PSI = 44

    Fahrenheit = 50
    Celsius = 51
    Kelvin = 52
    Rankin = 53

    MPS = 60
    KMH = 61
    FPS = 62
    MPH = 63
    KT = 64

    Grain = 70
    Ounce = 71
    Gram = 72
    Pound = 73
    Kilogram = 74
    Newton = 75

    def __call__(self, unit_type: 'AbstractUnit'):
        return unit_type.get_in(self)


class AbstractUnit(ABC):

    def __init__(self, value: float, units: Unit):
        self._value = self.to_default(value, units)
        self._defined_units = units

    def __str__(self):
        units = self._defined_units
        v = self.from_default(self._value, units)
        return f'{round(v, self.accuracy(units))} {self.name(units)}'

    def __repr__(self):
        return f'<{self.__class__.__name__}>'

    def to_default(self, value: float, units: Unit):
        raise KeyError(f'{self.__class__.__name__}: unit {units} is not supported')

    def from_default(self, value: float, units: Unit):
        raise KeyError(f'{self.__class__.__name__}: unit {units} is not supported')

    def value(self):
        return self._value

    def convert(self, units: Unit):
        value = self.get_in(units)
        return self.__class__(value, units)

    def get_in(self, units: Unit):
        return self.from_default(self._value, units)

    def units(self):
        return self._defined_units

    def default_value(self):
        return self._value

    @staticmethod
    def accuracy(units):
        return 6

    @staticmethod
    def name(units):
        return ""


class Distance(AbstractUnit):

    def to_default(self, value: float, units: Unit):
        if units == Distance.Inch:
            return value
        elif units == Distance.Foot:
            return value * 12
        elif units == Distance.Yard:
            return value * 36
        elif units == Distance.Mile:
            return value * 63360
        elif units == Distance.NauticalMile:
            return value * 72913.3858
        elif units == Distance.Line:
            return value / 10
        elif units == Distance.Millimeter:
            return value / 25.4
        elif units == Distance.Centimeter:
            return value / 2.54
        elif units == Distance.Meter:
            return value / 25.4 * 1000
        elif units == Distance.Kilometer:
            return value / 25.4 * 1000000
        super(Distance, self).to_default(value, units)

    def from_default(self, value: float, units: Unit):
        if units == Distance.Inch:
            return value
        elif units == Distance.Foot:
            return value / 12
        elif units == Distance.Yard:
            return value / 36
        elif units == Distance.Mile:
            return value / 63360
        elif units == Distance.NauticalMile:
            return value / 72913.3858
        elif units == Distance.Line:
            return value * 10
        elif units == Distance.Millimeter:
            return value * 25.4
        elif units == Distance.Centimeter:
            return value * 2.54
        elif units == Distance.Meter:
            return value * 25.4 / 1000
        elif units == Distance.Kilometer:
            return value * 25.4 / 1000000
        super(Distance, self).from_default(value, units)

    @staticmethod
    def name(units: Unit):
        if units == Distance.Inch:
            name = 'inch'
        elif units == Distance.Foot:
            name = 'ft'
        elif units == Distance.Yard:
            name = 'yd'
        elif units == Distance.Mile:
            name = 'mi'
        elif units == Distance.NauticalMile:
            name = 'nm'
        elif units == Distance.Line:
            name = 'ln'
        elif units == Distance.Millimeter:
            name = 'mm'
        elif units == Distance.Centimeter:
            name = 'cm'
        elif units == Distance.Meter:
            name = 'm'
        elif units == Distance.Kilometer:
            name = 'km'
        else:
            name = '?'
        return name

    @staticmethod
    def accuracy(units: Unit):
        if units == Distance.Inch:
            accuracy = 1
        elif units == Distance.Foot:
            accuracy = 2
        elif units == Distance.Yard:
            accuracy = 3
        elif units == Distance.Mile:
            accuracy = 3
        elif units == Distance.NauticalMile:
            accuracy = 3
        elif units == Distance.Line:
            accuracy = 1
        elif units == Distance.Millimeter:
            accuracy = 0
        elif units == Distance.Centimeter:
            accuracy = 1
        elif units == Distance.Meter:
            accuracy = 2
        elif units == Distance.Kilometer:
            accuracy = 3
        else:
            accuracy = 6
        return accuracy

    Inch = Unit.Inch
    Foot = Unit.Foot
    Yard = Unit.Yard
    Mile = Unit.Mile
    NauticalMile = Unit.NauticalMile
    Millimeter = Unit.Millimeter
    Centimeter = Unit.Centimeter
    Meter = Unit.Meter
    Kilometer = Unit.Kilometer
    Line = Unit.Line


class Pressure(AbstractUnit):

    def to_default(self, value: float, units: Unit):
        if units == Pressure.MmHg:
            return value
        elif units == Pressure.InHg:
            return value * 25.4
        elif units == Pressure.Bar:
            return value * 750.061683
        elif units == Pressure.HP:
            return value * 750.061683 / 1000
        elif units == Pressure.PSI:
            return value * 51.714924102396
        super(Pressure, self).to_default(value, units)

    def from_default(self, value: float, units: Unit):
        if units == Pressure.MmHg:
            return value
        elif units == Pressure.InHg:
            return value / 25.4
        elif units == Pressure.Bar:
            return value / 750.061683
        elif units == Pressure.HP:
            return value / 750.061683 * 1000
        elif units == Pressure.PSI:
            return value / 51.714924102396
        super(Pressure, self).from_default(value, units)

    @staticmethod
    def name(units: Unit):
        if units == Pressure.MmHg:
            name = 'mmHg'
        elif units == Pressure.MmHg:
            name = 'inHg'
        elif units == Pressure.Bar:
            name = 'bar'
        elif units == Pressure.HP:
            name = 'hPa'
        elif units == Pressure.PSI:
            name = 'psi'
        else:
            name = '?'
        return name

    @staticmethod
    def accuracy(units: Unit):
        if units == Pressure.MmHg:
            accuracy = 0
        elif units == Pressure.MmHg:
            accuracy = 2
        elif units == Pressure.Bar:
            accuracy = 2
        elif units == Pressure.HP:
            accuracy = 4
        elif units == Pressure.PSI:
            accuracy = 4
        else:
            accuracy = 6
        return accuracy

    # def __str__(self):
    #     default = self._defined_units
    #     v = self.from_default(self._value, default)
    #     if default == Pressure.MmHg:
    #         name = 'mmHg'
    #         accuracy = 0
    #     elif default == Pressure.MmHg:
    #         name = 'inHg'
    #         accuracy = 2
    #     elif default == Pressure.Bar:
    #         name = 'bar'
    #         accuracy = 2
    #     elif default == Pressure.HP:
    #         name = 'hPa'
    #         accuracy = 4
    #     elif default == Pressure.PSI:
    #         name = 'psi'
    #         accuracy = 4
    #     else:
    #         name = '?'
    #         accuracy = 6
    #
    #     return f'{round(v, accuracy)} {name}'

    MmHg = Unit.MmHg
    InHg = Unit.InHg
    Bar = Unit.Bar
    HP = Unit.HP
    PSI = Unit.PSI


class Weight(AbstractUnit):

    def to_default(self, value: float, units: Unit):
        if units == Weight.Grain:
            return value
        elif units == Weight.Gram:
            return value * 15.4323584
        elif units == Weight.Kilogram:
            return value * 15432.3584
        elif units == Weight.Newton:
            return value * 151339.73750336
        elif units == Weight.Pound:
            return value / 0.000142857143
        elif units == Weight.Ounce:
            return value * 437.5
        super(Weight, self).to_default(value, units)

    def from_default(self, value: float, units: Unit):
        if units == Weight.Grain:
            return value
        elif units == Weight.Gram:
            return value / 15.4323584
        elif units == Weight.Kilogram:
            return value / 15432.3584
        elif units == Weight.Newton:
            return value / 151339.73750336
        elif units == Weight.Pound:
            return value * 0.000142857143
        elif units == Weight.Ounce:
            return value / 437.5
        super(Weight, self).from_default(value, units)

    @staticmethod
    def name(units):

        if units == Weight.Grain:
            name = 'gr'
        elif units == Weight.Gram:
            name = 'g'
        elif units == Weight.Kilogram:
            name = 'kg'
        elif units == Weight.Newton:
            name = 'N'
        elif units == Weight.Pound:
            name = 'lb'
        elif units == Weight.Ounce:
            name = 'oz'
        else:
            name = '?'
        return name

    @staticmethod
    def accuracy(units):
        if units == Weight.Grain:
            accuracy = 0
        elif units == Weight.Gram:
            accuracy = 1
        elif units == Weight.Kilogram:
            accuracy = 3
        elif units == Weight.Newton:
            accuracy = 3
        elif units == Weight.Pound:
            accuracy = 3
        elif units == Weight.Ounce:
            accuracy = 1
        else:
            accuracy = 6
        return accuracy

    Grain = Unit.Grain
    Ounce = Unit.Ounce
    Gram = Unit.Gram
    Pound = Unit.Pound
    Kilogram = Unit.Kilogram
    Newton = Unit.Newton


class Temperature(AbstractUnit):

    def to_default(self, value: float, units: Unit):
        if units == Temperature.Fahrenheit:
            return value
        elif units == Temperature.Rankin:
            return value - 459.67
        elif units == Temperature.Celsius:
            return value * 9 / 5 + 32
        elif units == Temperature.Kelvin:
            return (value - 273.15) * 9 / 5 + 32
        super(Temperature, self).to_default(value, units)

    def from_default(self, value: float, units: Unit):
        if units == Temperature.Fahrenheit:
            return value
        elif units == Temperature.Rankin:
            return value + 459.67
        elif units == Temperature.Celsius:
            return (value - 32) * 5 / 9
        elif units == Temperature.Kelvin:
            return (value - 32) * 5 / 9 + 273.15
        super(Temperature, self).from_default(value, units)

    @staticmethod
    def name(units):
        if units == Temperature.Fahrenheit:
            name = '°F'
        elif units == Temperature.Rankin:
            name = '°R'
        elif units == Temperature.Celsius:
            name = '°C'
        elif units == Temperature.Kelvin:
            name = '°K'
        else:
            name = '?'
        return name

    @staticmethod
    def accuracy(units):
        if units == Temperature.Fahrenheit:
            accuracy = 1
        elif units == Temperature.Rankin:
            accuracy = 1
        elif units == Temperature.Celsius:
            accuracy = 1
        elif units == Temperature.Kelvin:
            accuracy = 1
        else:
            accuracy = 6
        return accuracy

    Fahrenheit = Unit.Fahrenheit
    Celsius = Unit.Celsius
    Kelvin = Unit.Kelvin
    Rankin = Unit.Rankin


class Angular(AbstractUnit):

    def to_default(self, value: float, units: Unit):
        if units == Angular.Radian:
            return value
        elif units == Angular.Degree:
            return value / 180 * pi
        elif units == Angular.MOA:
            return value / 180 * pi / 60
        elif units == Angular.Mil:
            return value / 3200 * pi
        elif units == Angular.MRad:
            return value / 1000
        elif units == Angular.Thousand:
            return value / 3000 * pi
        elif units == Angular.InchesPer100Yd:
            return atan(value / 3600)
        elif units == Angular.CmPer100M:
            return atan(value / 10000)
        super(Angular, self).to_default(value, units)

    def from_default(self, value: float, units: Unit):
        if units == Angular.Radian:
            return value
        elif units == Angular.Degree:
            return value * 180 / pi
        elif units == Angular.MOA:
            return value * 180 / pi * 60
        elif units == Angular.Mil:
            return value * 3200 / pi
        elif units == Angular.MRad:
            return value * 1000
        elif units == Angular.Thousand:
            return value * 3000 / pi
        elif units == Angular.InchesPer100Yd:
            return tan(value) * 3600
        elif units == Angular.CmPer100M:
            return tan(value) * 10000
        super(Angular, self).from_default(value, units)

    @staticmethod
    def name(units):
        if units == Angular.Radian:
            name = 'rad'
        elif units == Angular.Degree:
            name = '°'
        elif units == Angular.MOA:
            name = 'moa'
        elif units == Angular.Mil:
            name = 'mil'
        elif units == Angular.MRad:
            name = 'mrad'
        elif units == Angular.Thousand:
            name = 'ths'
        elif units == Angular.InchesPer100Yd:
            name = 'in/100yd'
        elif units == Angular.CmPer100M:
            name = 'cm/100m'
        else:
            name = '?'
        return name

    @staticmethod
    def accuracy(units):
        if units == Angular.Radian:
            accuracy = 6
        elif units == Angular.Degree:
            accuracy = 4
        elif units == Angular.MOA:
            accuracy = 2
        elif units == Angular.Mil:
            accuracy = 2
        elif units == Angular.MRad:
            accuracy = 2
        elif units == Angular.Thousand:
            accuracy = 2
        elif units == Angular.InchesPer100Yd:
            accuracy = 2
        elif units == Angular.CmPer100M:
            accuracy = 2
        else:
            accuracy = 6
        return accuracy

    Radian = Unit.Radian
    Degree = Unit.Degree
    MOA = Unit.MOA
    Mil = Unit.Mil
    MRad = Unit.MRad
    Thousand = Unit.Thousand
    InchesPer100Yd = Unit.InchesPer100Yd
    CmPer100M = Unit.CmPer100M


class Velocity(AbstractUnit):

    def to_default(self, value: float, units: Unit):
        if units == Velocity.MPS:
            return value
        elif units == Velocity.KMH:
            return value / 3.6
        elif units == Velocity.FPS:
            return value / 3.2808399
        elif units == Velocity.MPH:
            return value / 2.23693629
        elif units == Velocity.KT:
            return value / 1.94384449
        super(Velocity, self).to_default(value, units)

    def from_default(self, value: float, units: Unit):
        if units == Velocity.MPS:
            return value
        elif units == Velocity.KMH:
            return value * 3.6
        elif units == Velocity.FPS:
            return value * 3.2808399
        elif units == Velocity.MPH:
            return value * 2.23693629
        elif units == Velocity.KT:
            return value * 1.94384449
        super(Velocity, self).from_default(value, units)

    @staticmethod
    def name(units):
        if units == Velocity.MPS:
            name = "m/s"
        elif units == Velocity.KMH:
            name = "km/h"
        elif units == Velocity.FPS:
            name = "ft/s"
        elif units == Velocity.MPH:
            name = "mph"
        elif units == Velocity.KT:
            name = "kt"
        else:
            name = '?'
        return name

    @staticmethod
    def accuracy(units):
        if units == Velocity.MPS:
            accuracy = 0
        elif units == Velocity.KMH:
            accuracy = 1
        elif units == Velocity.FPS:
            accuracy = 1
        elif units == Velocity.MPH:
            accuracy = 1
        elif units == Velocity.KT:
            accuracy = 1
        else:
            accuracy = 6
        return accuracy

    MPS = Unit.MPS
    KMH = Unit.KMH
    FPS = Unit.FPS
    MPH = Unit.MPH
    KT = Unit.KT


class Energy(AbstractUnit):

    def to_default(self, value: float, units: int):
        if units == Energy.FootPound:
            return value
        elif units == Energy.Joule:
            return value * 0.737562149277
        else:
            raise KeyError(f'{self.__name__}: unit {units} is not supported')

    def from_default(self, value: float, units: int):
        if units == Energy.FootPound:
            return value
        elif units == Energy.Joule:
            return value / 0.737562149277
        else:
            raise KeyError(f'KeyError: {self.__name__}: unit {units} is not supported')

    @staticmethod
    def name(units):
        if units == Energy.FootPound:
            name = "ft·lb"
        elif units == Energy.Joule:
            name = "J"
        else:
            name = '?'
        return name

    @staticmethod
    def accuracy(units):
        if units == Energy.FootPound:
            accuracy = 0
        elif units == Energy.Joule:
            accuracy = 0
        else:
            accuracy = 6
        return accuracy

    FootPound = Unit.FootPound
    Joule = Unit.Joule


class Convertor:
    def __init__(self, measure=None, unit: int = 0, default_unit: int = 0):
        self.measure = measure
        self.unit = unit
        self.default_unit = default_unit

    def fromRaw(self, value):
        return self.measure(value, self.default_unit).get_in(self.unit)

    def toRaw(self, value):
        return self.measure(value, self.unit).get_in(self.default_unit)

    @property
    def accuracy(self):
        return self.measure.accuracy(self.unit)

    @property
    def unit_name(self):
        return self.measure.name(self.unit)
