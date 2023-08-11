import json
from kvgui.modules import signals as sig

DEFAULT_SETTINGS = {
  "lang": "English",
  "theme": "Dark",
  "unit_sight_height": 16,
  "unit_twist": 10,
  "unit_velocity": 60,
  "unit_distance": 17,
  "unit_temperature": 51,
  "unit_weight": 70,
  "unit_length": 10,
  "unit_diameter": 10,
  "unit_pressure": 40,
  "unit_drop": 16,
  "unit_angular": 1,
  "unit_adjustment": 7,
  "unit_energy": 30
}


class AppSettings:
    def __init__(self):
        self._dict: dict = dict()
        self.load_settings()
        # self.apply_settings()

    def __getattr__(self, name):
        if name != '_dict':
            value = self._dict.get(name)
            if value:
                return value

    def update(self, **kwargs):
        print("update:", kwargs)
        self._dict.update(kwargs)

    def load_settings(self):
        try:
            with open('kvgui/settings.json', 'r', encoding='utf-8') as fp:
                config = json.load(fp)
                for k, v in DEFAULT_SETTINGS.items():
                    if k not in config:
                        config[k] = DEFAULT_SETTINGS[k]
                self._dict = config
        except Exception:
            self._dict = DEFAULT_SETTINGS
        print(self._dict)

    def save_settings(self):
        try:
            with open('kvgui/settings.json', 'w', encoding='utf-8') as fp:
                json.dump(self._dict, fp)
        except Exception:
            pass

    def bind_on_load(self):
        sig.load_set_theme.emit(theme=self.theme)
        sig.load_set_lang.emit(lang=self.lang)

        sig.load_unit_sight_height.emit(unit=self.unit_sight_height)
        sig.load_unit_twist.emit(unit=self.unit_twist)
        sig.load_unit_velocity.emit(unit=self.unit_velocity)
        sig.load_unit_distance.emit(unit=self.unit_distance)
        sig.load_unit_temperature.emit(unit=self.unit_temperature)
        sig.load_unit_weight.emit(unit=self.unit_weight)

        sig.load_unit_length.emit(unit=self.unit_length)
        sig.load_unit_diameter.emit(unit=self.unit_diameter)
        sig.load_unit_pressure.emit(unit=self.unit_pressure)
        sig.load_unit_drop.emit(unit=self.unit_drop)
        sig.load_unit_angular.emit(unit=self.unit_angle)
        sig.load_unit_adjustment.emit(unit=self.unit_adjustment)
        sig.load_unit_energy.emit(unit=self.unit_energy)

        # for k, v in self._dict.items():
        #     sig.load_setting.emit(target=k, value=v)

    def bind_on_set(self):
        sig.set_theme.connect(self.update)
        sig.set_lang.connect(self.update)

        sig.set_unit_velocity.connect(lambda unit, **kw: self.update(unit_velocity=unit))
        sig.set_unit_distance.connect(lambda unit, **kw: self.update(unit_distance=unit))
        sig.set_unit_temperature.connect(lambda unit, **kw: self.update(unit_temperature=unit))
        sig.set_unit_weight.connect(lambda unit, **kw: self.update(unit_weight=unit))

        sig.set_unit_length.connect(lambda unit, **kw: self.update(unit_length=unit))
        sig.set_unit_diameter.connect(lambda unit, **kw: self.update(unit_diameter=unit))
        sig.set_unit_pressure.connect(lambda unit, **kw: self.update(unit_pressure=unit))
        sig.set_unit_drop.connect(lambda unit, **kw: self.update(unit_drop=unit))
        sig.set_unit_angular.connect(lambda unit, **kw: self.update(unit_angle=unit))
        sig.set_unit_adjustment.connect(lambda unit, **kw: self.update(unit_adjustment=unit))
        sig.set_unit_energy.connect(lambda unit, **kw: self.update(unit_energy=unit))

        sig.set_setting.connect(self.update)


app_settings = AppSettings()
