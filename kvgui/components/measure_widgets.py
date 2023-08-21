from kivy.lang import Builder

from kvgui.components.numeric_field import MDNumericField
from units import *
from units.ext import SmallDistance, BigDistance

measure_value_helper = """
<MeasureValue>
    size_hint_x: 0.3
    pos_hint: {'center_x': 0.5, 'center_y': 0.6}
    halign: 'right'
"""

Builder.load_string(measure_value_helper)


class MeasureValue(MDNumericField):
    def __init__(self, *args, **kwargs):
        super(MeasureValue, self).__init__(*args, **kwargs)
        self._convertor = None

    @property
    def convertor(self):
        return self._convertor

    @convertor.setter
    def convertor(self, value: Convertor):
        self._convertor = value
        self.decimals = value.measure.accuracy(value.unit)

    @property
    def measure(self):
        return self.convertor.measure

    @property
    def unit(self):
        return self.convertor.unit

    @unit.setter
    def unit(self, unit: Unit):
        if unit:
            self.convertor = Convertor(self.convertor.measure, unit, self.convertor.default_unit)

    @property
    def raw_value(self):
        if self._convertor is not None:
            return self._convertor.toRaw(self.value)
        else:
            return self.value

    @raw_value.setter
    def raw_value(self, value):
        if self._convertor is not None:
            self.value = self._convertor.fromRaw(value)
        else:
            self.value = value


class PressureValue(MeasureValue):
    id = 'pressure'

    def __init__(self, *args, **kwargs):
        super(PressureValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Pressure, Pressure.MmHg, Pressure.MmHg)
        self.min_value = lambda: Pressure(500, Pressure.MmHg).get_in(self.unit)
        self.max_value = lambda: Pressure(1100, Pressure.MmHg).get_in(self.unit)
        self.step = 1


class TemperatureValue(MeasureValue):
    id = 'temperature'

    def __init__(self, *args, **kwargs):
        super(TemperatureValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Temperature, Temperature.Celsius, Temperature.Celsius)
        self.min_value = lambda: Temperature(-50, Temperature.Celsius).get_in(self.unit)
        self.max_value = lambda: Temperature(50, Temperature.Celsius).get_in(self.unit)


class DistanceValue(MeasureValue):
    id = 'distance'

    def __init__(self, *args, **kwargs):
        super(DistanceValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(BigDistance, Distance.Meter, Distance.Meter)
        self.min_value = lambda: Distance(0, Distance.Meter).get_in(self.unit)
        self.max_value = lambda: Distance(3000, Distance.Meter).get_in(self.unit)


class WeightValue(MeasureValue):
    id = 'weight'

    def __init__(self, *args, **kwargs):
        super(WeightValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Weight, Weight.Grain, Weight.Grain)
        self.min_value = lambda: Weight(0, Weight.Kilogram).get_in(self.unit)
        self.max_value = lambda: Weight(50, Weight.Kilogram).get_in(self.unit)
        self.decimals = 2
        self.step = lambda: Weight(0.5, Weight.Grain).get_in(self.unit)


class LookAngleValue(MeasureValue):
    id = 'look_angle'

    def __init__(self, *args, **kwargs):
        super(LookAngleValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Angular, Angular.Degree, Angular.Degree)
        self.min_value = lambda: Angular(0, Angular.Degree).get_in(self.unit)
        self.max_value = lambda: Angular(359, Angular.Degree).get_in(self.unit)


class SightHeightValue(MeasureValue):
    id = 'sight_height'

    def __init__(self, *args, **kwargs):
        super(SightHeightValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Distance, Distance.Centimeter, Distance.Centimeter)
        self.min_value = lambda: Distance(0.1, Distance.Centimeter).get_in(self.unit)
        self.max_value = lambda: Distance(20, Distance.Centimeter).get_in(self.unit)


class TwistValue(MeasureValue):
    id = 'twist'

    def __init__(self, *args, **kwargs):
        super(TwistValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Distance, Distance.Inch, Distance.Inch)
        self.min_value = lambda: Distance(0, Distance.Inch).get_in(self.unit)
        self.max_value = lambda: Distance(20, Distance.Inch).get_in(self.unit)


class AltitudeValue(MeasureValue):
    id = 'altitude'

    def __init__(self, *args, **kwargs):
        super(AltitudeValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Distance, Distance.Meter, Distance.Meter)
        self.min_value = lambda: Distance(0, Distance.Meter).get_in(self.unit)
        self.max_value = lambda: Distance(9000, Distance.Meter).get_in(self.unit)


class WindSpeedValue(MeasureValue):
    id = 'wind_speed'

    def __init__(self, *args, **kwargs):
        super(WindSpeedValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Velocity, Velocity.MPS, Velocity.MPS)
        self.min_value = lambda: Velocity(0, Velocity.KMH).get_in(self.unit)
        self.max_value = lambda: Velocity(30, Velocity.KMH).get_in(self.unit)


class WindAngleValue(MeasureValue):
    id = 'wind_angle'

    def __init__(self, *args, **kwargs):
        super(WindAngleValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Angular, Angular.Degree, Angular.Degree)
        self.min_value = lambda: Angular(0, Angular.Degree).get_in(self.unit)
        self.max_value = lambda: Angular(359, Angular.Degree).get_in(self.unit)


class DiameterValue(MeasureValue):
    id = 'diameter'

    def __init__(self, *args, **kwargs):
        super(DiameterValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(SmallDistance, Distance.Inch, Distance.Inch)
        self.min_value = lambda: Distance(0, Distance.Millimeter).get_in(self.unit)
        self.max_value = lambda: Distance(155, Distance.Millimeter).get_in(self.unit)


class LengthValue(MeasureValue):
    id = 'weight'

    def __init__(self, *args, **kwargs):
        super(LengthValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(SmallDistance, Distance.Inch, Distance.Inch)
        self.min_value = lambda: Distance(0, Distance.Meter).get_in(self.unit)
        self.max_value = lambda: Distance(1, Distance.Meter).get_in(self.unit)


class VelocityValue(MeasureValue):

    def __init__(self, *args, **kwargs):
        super(VelocityValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Velocity, Velocity.MPS, Velocity.MPS)
        self.min_value = lambda: Velocity(0, Velocity.FPS).get_in(self.unit)
        self.max_value = lambda: Velocity(5000, Velocity.FPS).get_in(self.unit)
        self.step = 1


class MuzzleValue(MeasureValue):
    id = 'muzzle_velocity'

    def __init__(self, *args, **kwargs):
        super(MuzzleValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Velocity, Velocity.MPS, Velocity.MPS)
        self.min_value = lambda: Velocity(0, Velocity.FPS).get_in(self.unit)
        self.max_value = lambda: Velocity(5000, Velocity.FPS).get_in(self.unit)
        self.step = 1


class PowderTempValue(MeasureValue):
    id = 'powder_temp'

    def __init__(self, *args, **kwargs):
        super(PowderTempValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Temperature, Temperature.Celsius, Temperature.Celsius)
        self.min_value = lambda: Temperature(-50, Temperature.Celsius).get_in(self.unit)
        self.max_value = lambda: Temperature(50, Temperature.Celsius).get_in(self.unit)


class ZeroDistValue(MeasureValue):
    id = 'zero_dist'

    def __init__(self, *args, **kwargs):
        super(ZeroDistValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(BigDistance, Distance.Meter, Distance.Meter)
        self.min_value = lambda: Distance(0, Distance.Meter).get_in(self.unit)
        self.max_value = lambda: Distance(1000, Distance.Meter).get_in(self.unit)


class PowderSensValue(MeasureValue):
    id = 'powder_sens'

    def __init__(self, *args, **kwargs):
        super(PowderSensValue, self).__init__(*args, **kwargs)
        self.min_value = 0
        self.max_value = 100
        self.step = 0.01


class HumidityValue(MeasureValue):
    id = 'humidity'

    def __init__(self, *args, **kwargs):
        super(HumidityValue, self).__init__(*args, **kwargs)
        self.min_value = 0
        self.max_value = 100
        self.decimals = 1
        self.step = 1


class BCValue(MeasureValue):
    id = 'bc'

    def __init__(self, *args, **kwargs):
        super(BCValue, self).__init__(*args, **kwargs)
        self.min_value = 0.001
        self.max_value = 2
        self.decimals = 3
        self.step = 0.001


class MachValue(MeasureValue):
    id = 'mach'

    def __init__(self, *args, **kwargs):
        super(MachValue, self).__init__(*args, **kwargs)
        self.min_value = 0
        self.max_value = 5
        self.decimals = 2
        self.step = 0.05


class CDValue(MeasureValue):
    id = 'cd'

    def __init__(self, *args, **kwargs):
        super(CDValue, self).__init__(*args, **kwargs)
        self.min_value = 0
        self.max_value = 1
        self.decimals = 3
        self.step = 0.001
