from kivy.lang import Builder

from kvgui.components.numeric_field import MDNumericField
from units import *

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


class DistanceValue(MeasureValue):
    id = 'distance'
    def __init__(self, *args, **kwargs):
        super(DistanceValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Distance, Distance.Meter, Distance.Meter)


class AngularValue(MeasureValue):
    id = 'angular'
    def __init__(self, *args, **kwargs):
        super(AngularValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Angular, Angular.Degree, Angular.Degree)


class PressureValue(MeasureValue):
    id = 'pressure'
    def __init__(self, *args, **kwargs):
        super(PressureValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Pressure, Pressure.MmHg, Pressure.MmHg)


class TemperatureValue(MeasureValue):
    id = 'temperature'
    def __init__(self, *args, **kwargs):
        super(TemperatureValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Temperature, Temperature.Celsius, Temperature.Celsius)


class VelocityValue(MeasureValue):
    id = 'velocity'
    def __init__(self, *args, **kwargs):
        super(VelocityValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Velocity, Velocity.MPS, Velocity.MPS)


class WeightValue(MeasureValue):
    id = 'weight'
    def __init__(self, *args, **kwargs):
        super(WeightValue, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Weight, Weight.Grain, Weight.Grain)


class LookAngleValue(AngularValue):
    id = 'look_angle'


class SightHeightValue(DistanceValue):
    id = 'sight_height'


class TwistValue(DistanceValue):
    id = 'twist'


class AltitudeValue(DistanceValue):
    id = 'altitude'


class WindSpeedValue(VelocityValue):
    id = 'wind_speed'


class WindAngleValue(AngularValue):
    id = 'wind_angle'


class DiameterValue(DistanceValue):
    id = 'diameter'


class LengthValue(DistanceValue):
    id = 'weight'


class MuzzleValue(VelocityValue):
    id = 'muzzle_velocity'


class PowderTempValue(TemperatureValue):
    id = 'powder_temp'


class ZeroDistValue(DistanceValue):
    id = 'zero_dist'
