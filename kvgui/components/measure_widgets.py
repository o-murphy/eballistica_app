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


class PercentMeasure(MeasureValue):
    def __init__(self, *args, **kwargs):
        super(PercentMeasure, self).__init__(*args, **kwargs)


class DistanceMeasure(MeasureValue):

    def __init__(self, *args, **kwargs):
        super(DistanceMeasure, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Distance, Distance.Meter, Distance.Meter)


class AngularMeasure(MeasureValue):

    def __init__(self, *args, **kwargs):
        super(AngularMeasure, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Angular, Angular.Degree, Angular.Degree)


class PressureMeasure(MeasureValue):

    def __init__(self, *args, **kwargs):
        super(PressureMeasure, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Pressure, Pressure.MmHg, Pressure.MmHg)


class TemperatureMeasure(MeasureValue):

    def __init__(self, *args, **kwargs):
        super(TemperatureMeasure, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Temperature, Temperature.Celsius, Temperature.Celsius)


class VelocityMeasure(MeasureValue):

    def __init__(self, *args, **kwargs):
        super(VelocityMeasure, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Velocity, Velocity.MPS, Velocity.MPS)


class WeightMeasure(MeasureValue):

    def __init__(self, *args, **kwargs):
        super(WeightMeasure, self).__init__(*args, **kwargs)
        self.convertor = Convertor(Weight, Weight.Grain, Weight.Grain)


class SmallDistMeasure(MeasureValue):

    def __init__(self, *args, **kwargs):
        super(SmallDistMeasure, self).__init__(*args, **kwargs)
        self.convertor = Convertor(SmallDistance, Distance.Inch, Distance.Inch)


class BigDistMeasure(MeasureValue):

    def __init__(self, *args, **kwargs):
        super(BigDistMeasure, self).__init__(*args, **kwargs)
        self.convertor = Convertor(BigDistance, Distance.Inch, Distance.Inch)


class PressureValue(PressureMeasure):
    id = 'pressure'

    def __init__(self, *args, **kwargs):
        super(PressureValue, self).__init__(*args, **kwargs)
        self.min_value = lambda: Pressure(500, Pressure.MmHg).get_in(self.unit)
        self.max_value = lambda: Pressure(1100, Pressure.MmHg).get_in(self.unit)


class TemperatureValue(TemperatureMeasure):
    id = 'temperature'

    def __init__(self, *args, **kwargs):
        super(TemperatureValue, self).__init__(*args, **kwargs)
        self.min_value = lambda: Temperature(-50, Temperature.Celsius).get_in(self.unit)
        self.max_value = lambda: Temperature(50, Temperature.Celsius).get_in(self.unit)


class DistanceValue(BigDistMeasure):
    id = 'distance'

    def __init__(self, *args, **kwargs):
        super(DistanceValue, self).__init__(*args, **kwargs)
        self.min_value = lambda: Distance(0, Distance.Meter).get_in(self.unit)
        self.max_value = lambda: Distance(3000, Distance.Meter).get_in(self.unit)
        

class WeightValue(WeightMeasure):
    id = 'weight'

    def __init__(self, *args, **kwargs):
        super(WeightValue, self).__init__(*args, **kwargs)
        self.min_value = lambda: Weight(0, Weight.Kilogram).get_in(self.unit)
        self.max_value = lambda: Weight(50, Weight.Kilogram).get_in(self.unit)
        self.decimals = 2
        self.step = lambda: Weight(0.5, Weight.Grain).get_in(self.unit)


class LookAngleValue(AngularMeasure):
    id = 'look_angle'

    def __init__(self, *args, **kwargs):
        super(LookAngleValue, self).__init__(*args, **kwargs)
        self.min_value = lambda: Angular(0, Angular.Degree).get_in(self.unit)
        self.max_value = lambda: Angular(359, Angular.Degree).get_in(self.unit)


class SightHeightValue(DistanceMeasure):
    id = 'sight_height'

    def __init__(self, *args, **kwargs):
        super(SightHeightValue, self).__init__(*args, **kwargs)
        self.min_value = lambda: Distance(0, Distance.Centimeter).get_in(self.unit)
        self.max_value = lambda: Distance(20, Distance.Centimeter).get_in(self.unit)


class TwistValue(DistanceMeasure):
    id = 'twist'

    def __init__(self, *args, **kwargs):
        super(TwistValue, self).__init__(*args, **kwargs)
        self.min_value = lambda: Distance(0, Distance.Inch).get_in(self.unit)
        self.max_value = lambda: Distance(20, Distance.Inch).get_in(self.unit)


class AltitudeValue(DistanceMeasure):
    id = 'altitude'

    def __init__(self, *args, **kwargs):
        super(AltitudeValue, self).__init__(*args, **kwargs)
        self.min_value = lambda: Distance(0, Distance.Meter).get_in(self.unit)
        self.max_value = lambda: Distance(9000, Distance.Meter).get_in(self.unit)


class WindSpeedValue(VelocityMeasure):
    id = 'wind_speed'

    def __init__(self, *args, **kwargs):
        super(WindSpeedValue, self).__init__(*args, **kwargs)
        self.min_value = lambda: Velocity(0, Velocity.KMH).get_in(self.unit)
        self.max_value = lambda: Velocity(15, Velocity.KMH).get_in(self.unit)


class WindAngleValue(AngularMeasure):
    id = 'wind_angle'

    def __init__(self, *args, **kwargs):
        super(WindAngleValue, self).__init__(*args, **kwargs)
        self.min_value = lambda: Angular(0, Angular.Degree).get_in(self.unit)
        self.max_value = lambda: Angular(359, Angular.Degree).get_in(self.unit)


class DiameterValue(SmallDistMeasure):
    id = 'diameter'

    def __init__(self, *args, **kwargs):
        super(DiameterValue, self).__init__(*args, **kwargs)
        self.min_value = lambda: Distance(0, Distance.Millimeter).get_in(self.unit)
        self.max_value = lambda: Distance(155, Distance.Millimeter).get_in(self.unit)


class LengthValue(SmallDistMeasure):
    id = 'weight'

    def __init__(self, *args, **kwargs):
        super(LengthValue, self).__init__(*args, **kwargs)
        self.min_value = lambda: Distance(0, Distance.Meter).get_in(self.unit)
        self.max_value = lambda: Distance(1, Distance.Meter).get_in(self.unit)


class MuzzleValue(VelocityMeasure):
    id = 'muzzle_velocity'

    def __init__(self, *args, **kwargs):
        super(MuzzleValue, self).__init__(*args, **kwargs)
        self.min_value = lambda: Velocity(10, Velocity.FPS).get_in(self.unit)
        self.max_value = lambda: Velocity(5000, Velocity.FPS).get_in(self.unit)


class PowderTempValue(TemperatureValue):
    id = 'powder_temp'

    def __init__(self, *args, **kwargs):
        super(PowderTempValue, self).__init__(*args, **kwargs)
        self.min_value = lambda: Temperature(-50, Temperature.Celsius).get_in(self.unit)
        self.max_value = lambda: Temperature(50, Temperature.Celsius).get_in(self.unit)


class ZeroDistValue(BigDistMeasure):
    id = 'zero_dist'
    
    def __init__(self, *args, **kwargs):
        super(ZeroDistValue, self).__init__(*args, **kwargs)
        self.min_value = lambda: Distance(0, Distance.Meter).get_in(self.unit)
        self.max_value = lambda: Distance(1000, Distance.Meter).get_in(self.unit)


class PowderSensValue(PercentMeasure):
    id = 'powder_sens'

    def __init__(self, *args, **kwargs):
        super(PowderSensValue, self).__init__(*args, **kwargs)
        self.min_value = 0
        self.max_value = 100
        self.step = 0.01


class HumidityValue(PercentMeasure):
    id = 'humidity'

    def __init__(self, *args, **kwargs):
        super(HumidityValue, self).__init__(*args, **kwargs)
        self.min_value = 0
        self.max_value = 100
        self.decimals = 1
        self.step = 1

