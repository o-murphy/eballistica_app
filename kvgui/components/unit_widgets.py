from kvgui.components.abstract import UnitSelector
from units import *


class TwistUnits(UnitSelector):
    def __init__(self, *args, **kwargs):
        super(TwistUnits, self).__init__(*args, **kwargs)
        self.id = 'unit_twist'
        self.unit_class = Distance
        self.units_specified = (Distance.Inch, Distance.Centimeter, Distance.Millimeter, Distance.Line)


class SightHeightUnits(UnitSelector):
    def __init__(self, *args, **kwargs):
        super(SightHeightUnits, self).__init__(*args, **kwargs)
        self.id = 'unit_sight_height'
        self.unit_class = Distance
        self.units_specified = (Distance.Inch, Distance.Centimeter, Distance.Millimeter, Distance.Line)


class VelocityUnits(UnitSelector):
    def __init__(self, *args, **kwargs):
        super(VelocityUnits, self).__init__(*args, **kwargs)
        self.id = 'unit_velocity'
        self.unit_class = Velocity
        self.units_specified = (Velocity.MPS, Velocity.FPS, Velocity.KMH, Velocity.MPS, Velocity.KT)


class DistanceUnits(UnitSelector):
    def __init__(self, *args, **kwargs):
        super(DistanceUnits, self).__init__(*args, **kwargs)
        self.id = 'unit_distance'
        self.unit_class = Distance
        self.units_specified = (Distance.Meter, Distance.Kilometer, Distance.Foot,
                                Distance.Yard, Distance.Mile, Distance.NauticalMile)


class TemperatureUnits(UnitSelector):
    def __init__(self, *args, **kwargs):
        super(TemperatureUnits, self).__init__(*args, **kwargs)
        self.id = 'unit_temperature'
        self.unit_class = Temperature
        self.units_specified = (Temperature.Celsius, Temperature.Fahrenheit,
                                Temperature.Kelvin, Temperature.Rankin)


class WeightUnits(UnitSelector):
    def __init__(self, *args, **kwargs):
        super(WeightUnits, self).__init__(*args, **kwargs)
        self.id = 'unit_weight'
        self.unit_class = Weight
        self.units_specified = (Weight.Grain, Weight.Gram, Weight.Kilogram,
                                Weight.Pound, Weight.Newton, Weight.Ounce)


class LengthUnits(UnitSelector):
    def __init__(self, *args, **kwargs):
        super(LengthUnits, self).__init__(*args, **kwargs)
        self.id = 'unit_length'
        self.unit_class = Distance
        self.units_specified = (Distance.Inch, Distance.Centimeter, Distance.Millimeter, Distance.Line)


class DiameterUnits(UnitSelector):
    def __init__(self, *args, **kwargs):
        super(DiameterUnits, self).__init__(*args, **kwargs)
        self.id = 'unit_diameter'
        self.unit_class = Distance
        self.units_specified = (Distance.Inch, Distance.Centimeter, Distance.Millimeter, Distance.Line)


class PressureUnits(UnitSelector):
    def __init__(self, *args, **kwargs):
        super(PressureUnits, self).__init__(*args, **kwargs)
        self.id = 'unit_pressure'
        self.unit_class = Pressure
        self.units_specified = (Pressure.MmHg, Pressure.HP, Pressure.InHg, Pressure.Bar, Pressure.PSI)


class PropUnits(UnitSelector):
    def __init__(self, *args, **kwargs):
        super(PropUnits, self).__init__(*args, **kwargs)
        self.id = 'unit_drop'
        self.unit_class = Distance
        self.units_specified = (Distance.Centimeter, Distance.Inch, Distance.Millimeter, Distance.Line,
                                Distance.Meter, Distance.Kilometer, Distance.Foot, Distance.Yard,
                                Distance.Mile, Distance.NauticalMile)


class AngularUnits(UnitSelector):
    def __init__(self, *args, **kwargs):
        super(AngularUnits, self).__init__(*args, **kwargs)
        self.id = 'unit_angular'
        self.unit_class = Angular
        self.units_specified = (Angular.CmPer100M, Angular.Mil, Angular.MOA, Angular.MRad,
                                Angular.Radian, Angular.InchesPer100Yd, Angular.Thousand, Angular.Degree)


class AdjustmentUnits(UnitSelector):
    def __init__(self, *args, **kwargs):
        super(AdjustmentUnits, self).__init__(*args, **kwargs)
        self.id = 'unit_adjustment'
        self.unit_class = Angular
        self.units_specified = (Angular.CmPer100M, Angular.Mil, Angular.MOA, Angular.MRad,
                                Angular.Radian, Angular.InchesPer100Yd, Angular.Thousand, Angular.Degree)


class EnergyUnits(UnitSelector):
    def __init__(self, *args, **kwargs):
        super(EnergyUnits, self).__init__(*args, **kwargs)
        self.id = 'unit_energy'
        self.unit_class = Energy
        self.units_specified = (Energy.Joule, Energy.FootPound)
