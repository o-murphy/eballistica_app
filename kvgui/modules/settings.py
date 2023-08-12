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
        sig.load_setting.emit(**self._dict)

    def bind_on_set(self):
        sig.set_theme.connect(self.update)
        sig.set_lang.connect(self.update)
        sig.set_setting.connect(self.update)


app_settings = AppSettings()
