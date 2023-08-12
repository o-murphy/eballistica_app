from kivy.lang import Builder
from kvgui.components.numeric_field import MDNumericField
from units import Convertor, Distance, Unit
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
    def unit(self):
        return self.convertor.unit

    @unit.setter
    def unit(self, unit: Unit):
        print(unit)
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
        self.id = 'twist'
        self.convertor = Convertor(Distance, Distance.Meter, Distance.Meter)
