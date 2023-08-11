import json
from kvgui.modules import signals as sig

DEFAULT_SETTINGS = {
  "lang": "English",
  "theme": "Dark",
  "shUnits": 16,
  "twistUnits": 10,
  "vUnits": 60,
  "distUnits": 17,
  "tempUnits": 51,
  "wUnits": 70,
  "lnUnits": 10,
  "dUnits": 10,
  "pUnits": 40,
  "dropUnits": 16,
  "angleUnits": 1,
  "adjUnits": 7,
  "eUnits": 30
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

        sig.load_set_sh_unit_change.emit(unit=self.shUnits)
        sig.load_set_tw_unit_change.emit(unit=self.twistUnits)
        sig.load_set_v_unit_change.emit(unit=self.vUnits)
        sig.load_set_dt_unit_change.emit(unit=self.distUnits)
        sig.load_set_t_unit_change.emit(unit=self.tempUnits)
        sig.load_set_w_unit_change.emit(unit=self.wUnits)

        sig.load_set_ln_unit_change.emit(unit=self.lnUnits)
        sig.load_set_dm_unit_change.emit(unit=self.dUnits)
        sig.load_set_ps_unit_change.emit(unit=self.pUnits)
        sig.load_set_dp_unit_change.emit(unit=self.dropUnits)
        sig.load_set_an_unit_change.emit(unit=self.angleUnits)
        sig.load_set_ad_unit_change.emit(unit=self.adjUnits)
        sig.load_set_e_unit_change.emit(unit=self.eUnits)

    def bind_on_set(self):
        sig.set_theme_changed.connect(self.update)
        sig.set_lang_changed.connect(self.update)
        
        sig.set_sh_unit_change.connect(lambda unit, **kw: self.update(shUnits=unit))
        sig.set_tw_unit_change.connect(lambda unit, **kw: self.update(twistUnits=unit))
        sig.set_v_unit_change.connect(lambda unit, **kw: self.update(vUnits=unit))
        sig.set_dt_unit_change.connect(lambda unit, **kw: self.update(distUnits=unit))
        sig.set_t_unit_change.connect(lambda unit, **kw: self.update(tempUnits=unit))
        sig.set_w_unit_change.connect(lambda unit, **kw: self.update(wUnits=unit))

        sig.set_ln_unit_change.connect(lambda unit, **kw: self.update(lnUnits=unit))
        sig.set_dm_unit_change.connect(lambda unit, **kw: self.update(dUnits=unit))
        sig.set_ps_unit_change.connect(lambda unit, **kw: self.update(pUnits=unit))
        sig.set_dp_unit_change.connect(lambda unit, **kw: self.update(dropUnits=unit))
        sig.set_an_unit_change.connect(lambda unit, **kw: self.update(angleUnits=unit))
        sig.set_ad_unit_change.connect(lambda unit, **kw: self.update(adjUnits=unit))
        sig.set_e_unit_change.connect(lambda unit, **kw: self.update(eUnits=unit))


app_settings = AppSettings()
