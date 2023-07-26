from abc import ABC
from enum import Enum
from math import pi, atan, tan


class Unit(Enum):
    Inch = 'in'
    Foot = 'ft'
    Yard = 'yd'
    Mile = 'mi'
    NauticalMile = 'nm'
    Millimeter = 'mm'
    Centimeter = 'cm'
    Meter = 'm'
    Kilometer = 'lm'
    Line = 'ln'


class AbstractUnit(ABC):

    def __init__(self, value: float, units: int):
        self._value = self.to_default(value, units)
        self._defined_units = units

    def __str__(self):
        default = self._defined_units
        v = self.from_default(self._value, default)
        name = '?'
        accuracy = 6
        return f'{round(v, accuracy)} {name}'

    def __repr__(self):
        return f'<{self.__class__.__name__}>'

    def to_default(self, value: float, units: int):
        raise KeyError(f'{self.__class__.__name__}: unit {units} is not supported')

    def from_default(self, value: float, units: int):
        raise KeyError(f'{self.__class__.__name__}: unit {units} is not supported')

    def value(self, units: int):
        return self.from_default(self._value, units)

    def convert(self, units: int):
        value = self.get_in(units)
        return Distance(value, units)

    def get_in(self, units: int):
        return self.from_default(self._value, units)

    def units(self):
        return self._defined_units

    def default_value(self):
        return self._value


class Distance(AbstractUnit):

    def to_default(self, value: float, units: int):
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

    def from_default(self, value: float, units: int):
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

    def __str__(self):

        default = self._defined_units
        v = self.from_default(self._value, default)
        if default == Distance.Inch:
            name = 'in'
            accuracy = 1
        elif default == Distance.Foot:
            name = 'ft'
            accuracy = 2
        elif default == Distance.Yard:
            name = 'yd'
            accuracy = 3
        elif default == Distance.Mile:
            name = 'mi'
            accuracy = 3
        elif default == Distance.NauticalMile:
            name = 'nm'
            accuracy = 3
        elif default == Distance.Line:
            name = 'ln'
            accuracy = 1
        elif default == Distance.Millimeter:
            name = 'mm'
            accuracy = 0
        elif default == Distance.Centimeter:
            name = 'cm'
            accuracy = 1
        elif default == Distance.Meter:
            name = 'm'
            accuracy = 2
        elif default == Distance.Kilometer:
            name = 'km'
            accuracy = 3
        else:
            name = '?'
            accuracy = 6

        return f'{round(v, accuracy)} {name}'

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

    def to_default(self, value: float, units: int):
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

    def from_default(self, value: float, units: int):
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
        super(Pressure, self).from_default()

    def __str__(self):
        default = self._defined_units
        v = self.from_default(self._value, default)
        if default == Pressure.MmHg:
            name = 'mmHg'
            accuracy = 0
        elif default == Pressure.MmHg:
            name = 'inHg'
            accuracy = 2
        elif default == Pressure.Bar:
            name = 'bar'
            accuracy = 2
        elif default == Pressure.HP:
            name = 'hPa'
            accuracy = 4
        elif default == Pressure.PSI:
            name = 'psi'
            accuracy = 4
        else:
            name = '?'
            accuracy = 6

        return f'{round(v, accuracy)} {name}'

    MmHg = 40
    InHg = 41
    Bar = 42
    HP = 43
    PSI = 44


class Weight(AbstractUnit):

    def to_default(self, value: float, units: int):
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

    def from_default(self, value: float, units: int):
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

    def __str__(self):

        default = self._defined_units
        v = self.from_default(self._value, default)
        if default == Weight.Grain:
            name = 'gr'
            accuracy = 0
        elif default == Weight.Gram:
            name = 'g'
            accuracy = 1
        elif default == Weight.Kilogram:
            name = 'kg'
            accuracy = 3
        elif default == Weight.Newton:
            name = 'N'
            accuracy = 3
        elif default == Weight.Pound:
            name = 'lb'
            accuracy = 3
        elif default == Weight.Ounce:
            name = 'oz'
            accuracy = 1
        else:
            name = '?'
            accuracy = 6

        return f'{round(v, accuracy)} {name}'

    Grain = 70
    Ounce = 71
    Gram = 72
    Pound = 73
    Kilogram = 74
    Newton = 75


class Temperature(AbstractUnit):

    def to_default(self, value: float, units: int):
        if units == Temperature.Fahrenheit:
            return value
        elif units == Temperature.Rankin:
            return value - 459.67
        elif units == Temperature.Celsius:
            return value * 9 / 5 + 32
        elif units == Temperature.Kelvin:
            return (value - 273.15) * 9 / 5 + 32
        super(Temperature, self).to_default(value, units)

    def from_default(self, value: float, units: int):
        if units == Temperature.Fahrenheit:
            return value
        elif units == Temperature.Rankin:
            return value + 459.67
        elif units == Temperature.Celsius:
            return (value - 32) * 5 / 9
        elif units == Temperature.Kelvin:
            return (value - 32) * 5 / 9 + 273.15
        super(Temperature, self).from_default(value, units)

    def __str__(self):
        default = self._defined_units
        v = self.from_default(self._value, default)
        if default == Temperature.Fahrenheit:
            name = '°F'
            accuracy = 1
        elif default == Temperature.Rankin:
            name = '°R'
            accuracy = 1
        elif default == Temperature.Celsius:
            name = '°C'
            accuracy = 1
        elif default == Temperature.Kelvin:
            name = '°K'
            accuracy = 1
        else:
            name = '?'
            accuracy = 6
        return f'{round(v, accuracy)} {name}'

    Fahrenheit: int = 50
    Celsius: int = 51
    Kelvin: int = 52
    Rankin: int = 53


class Angular(AbstractUnit):

    def to_default(self, value: float, units: int):
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

    def from_default(self, value: float, units: int):
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

    def __str__(self):

        default = self._defined_units
        v = self.from_default(self._value, default)
        if default == Angular.Radian:
            name = 'rad'
            accuracy = 6
        elif default == Angular.Degree:
            name = '°'
            accuracy = 4
        elif default == Angular.MOA:
            name = 'moa'
            accuracy = 2
        elif default == Angular.Mil:
            name = 'mil'
            accuracy = 2
        elif default == Angular.MRad:
            name = 'mrad'
            accuracy = 2
        elif default == Angular.Thousand:
            name = 'ths'
            accuracy = 2
        elif default == Angular.InchesPer100Yd:
            name = 'in/100yd'
            accuracy = 2
        elif default == Angular.CmPer100M:
            name = 'cm/100m'
            accuracy = 2
        else:
            name = '?'
            accuracy = 6

        return f'{round(v, accuracy)} {name}'

    Radian = 0
    Degree = 1
    MOA = 2
    Mil = 3
    MRad = 4
    Thousand = 5
    InchesPer100Yd = 6
    CmPer100M = 7


class Velocity(AbstractUnit):

    def to_default(self, value: float, units: int):
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

    def from_default(self, value: float, units: int):
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

    def __str__(self):
        default = self._defined_units
        v = self.from_default(self._value, default)
        if default == Velocity.MPS:
            name = "m/s"
            accuracy = 0
        elif default == Velocity.KMH:
            name = "km/h"
            accuracy = 1
        elif default == Velocity.FPS:
            name = "ft/s"
            accuracy = 1
        elif default == Velocity.MPH:
            name = "mph"
            accuracy = 1
        elif default == Velocity.KT:
            name = "kt"
            accuracy = 1
        else:
            name = '?'
            accuracy = 6
        return f'{round(v, accuracy)} {name}'

    MPS = 60
    KMH = 61
    FPS = 62
    MPH = 63
    KT = 64
