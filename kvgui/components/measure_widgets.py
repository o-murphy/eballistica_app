from kivy.lang import Builder
from kvgui.components.numeric_field import MDNumericField
from units import *
import units.ext


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


class SightHeightValue(MeasureValue):
    def __init__(self, *args, **kwargs):
        super(SightHeightValue, self).__init__(*args, **kwargs)
        self.id = 'sight_height'
        self.convertor = Convertor(Distance, Distance.Centimeter, Distance.Centimeter)


class TwistValue(MeasureValue):
    def __init__(self, *args, **kwargs):
        super(TwistValue, self).__init__(*args, **kwargs)
        self.id = 'twist'
        self.convertor = Convertor(Distance, Distance.Centimeter, Distance.Centimeter)


class DistanceValue(MeasureValue):
    def __init__(self, *args, **kwargs):
        super(DistanceValue, self).__init__(*args, **kwargs)
        self.id = 'distance'
        self.convertor = Convertor(Distance, Distance.Meter, Distance.Meter)


class AltitudeValue(DistanceValue):
    def __init__(self, *args, **kwargs):
        super(AltitudeValue, self).__init__(*args, **kwargs)
        self.id = 'altitude'


class AngularValue(MeasureValue):
    def __init__(self, *args, **kwargs):
        super(AngularValue, self).__init__(*args, **kwargs)
        self.id = 'angular'
        self.convertor = Convertor(Angular, Angular.Degree, Angular.Degree)


class LookAngleValue(AngularValue):
    def __init__(self, *args, **kwargs):
        super(LookAngleValue, self).__init__(*args, **kwargs)
        self.id = 'look_angle'


class PressureValue(MeasureValue):
    def __init__(self, *args, **kwargs):
        super(PressureValue, self).__init__(*args, **kwargs)
        self.id = 'pressure'
        self.convertor = Convertor(Pressure, Pressure.MmHg, Pressure.MmHg)


class TemperatureValue(MeasureValue):
    def __init__(self, *args, **kwargs):
        super(TemperatureValue, self).__init__(*args, **kwargs)
        self.id = 'temperature'
        self.convertor = Convertor(Temperature, Temperature.Celsius, Temperature.Celsius)


class VelocityValue(MeasureValue):
    def __init__(self, *args, **kwargs):
        super(VelocityValue, self).__init__(*args, **kwargs)
        self.id = 'velocity'
        self.convertor = Convertor(Velocity, Velocity.MPS, Velocity.MPS)


class WindSpeedValue(VelocityValue):
    def __init__(self, *args, **kwargs):
        super(WindSpeedValue, self).__init__(*args, **kwargs)
        self.id = 'wind_speed'


class WindAngleValue(AngularValue):
    def __init__(self, *args, **kwargs):
        super(WindAngleValue, self).__init__(*args, **kwargs)
        self.id = 'wind_angle'
