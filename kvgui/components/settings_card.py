from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView


Builder.load_string("""
<CardTitle>
    font_style: 'H6'
    size_hint_y: None
    height: self.texture_size[1]

<MD3Card>
    orientation: "vertical"
    padding: "20dp"
    spacing: "15dp"
    height: self.minimum_height
    size_hint_y: None

<NamedSelector>
    orientation: "horizontal"
    height: self.minimum_height
    size_hint_y: None
    
<InScrollBox>
    orientation: "vertical"
    spacing: "15dp"
    padding: "20dp"
    height: self.minimum_height
    size_hint_y: None
""")


class NamedSelector(BoxLayout):
    def __init__(self, **kwargs):
        super(NamedSelector, self).__init__(**kwargs)
        self.init_ui()

    def init_ui(self):
        self.label = MDLabel(size_hint_x=.5)
        self.dropdown = MDDropDownItem(size_hint_x=.5)
        self.add_widget(self.label)
        self.add_widget(self.dropdown)


class ThemeSelector(NamedSelector):

    def init_ui(self):
        super(ThemeSelector, self).init_ui()
        self.label.text = 'Theme'


class LanguageSelector(NamedSelector):

    def init_ui(self):
        super(LanguageSelector, self).init_ui()
        self.label.text = 'Language'


class SightHeightUnitSelector(NamedSelector):

    def init_ui(self):
        super(SightHeightUnitSelector, self).init_ui()
        self.label.text = "Sight height"


class TwistUnitSelector(NamedSelector):

    def init_ui(self):
        super(TwistUnitSelector, self).init_ui()
        self.label.text = "Twist"


class VelocityUnitSelector(NamedSelector):

    def init_ui(self):
        super(VelocityUnitSelector, self).init_ui()
        self.label.text = "Velocity"


class DistanceUnitSelector(NamedSelector):

    def init_ui(self):
        super(DistanceUnitSelector, self).init_ui()
        self.label.text = "Distance"


class TemperatureUnitSelector(NamedSelector):

    def init_ui(self):
        super(TemperatureUnitSelector, self).init_ui()
        self.label.text = "Temperature"


class WeightUnitSelector(NamedSelector):

    def init_ui(self):
        super(WeightUnitSelector, self).init_ui()
        self.label.text = "Weight"


class LengthUnitSelector(NamedSelector):

    def init_ui(self):
        super(LengthUnitSelector, self).init_ui()
        self.label.text = "Length"


class DiameterUnitSelector(NamedSelector):

    def init_ui(self):
        super(DiameterUnitSelector, self).init_ui()
        self.label.text = "Diameter"


class PressureUnitSelector(NamedSelector):

    def init_ui(self):
        super(PressureUnitSelector, self).init_ui()
        self.label.text = "Pressure"


class PathUnitSelector(NamedSelector):

    def init_ui(self):
        super(PathUnitSelector, self).init_ui()
        self.label.text = "Path"


class AngularUnitSelector(NamedSelector):

    def init_ui(self):
        super(AngularUnitSelector, self).init_ui()
        self.label.text = "Angular"


class DropUnitSelector(NamedSelector):

    def init_ui(self):
        super(DropUnitSelector, self).init_ui()
        self.label.text = "Drop"


class EnergyUnitSelector(NamedSelector):

    def init_ui(self):
        super(EnergyUnitSelector, self).init_ui()
        self.label.text = "Energy"


class CardTitle(MDLabel):
    pass


class MD3Card(MDCard):
    def __init__(self, **kwargs):
        super(MD3Card, self).__init__(**kwargs)
        self.init_ui()

    def init_ui(self):
        self.title = CardTitle()
        self.add_widget(self.title)


class ViewCard(MD3Card):
    def init_ui(self):
        super(ViewCard, self).init_ui()
        self.title.text = 'View:'
        self.s_theme = ThemeSelector()
        self.s_lang = LanguageSelector()
        self.add_widget(self.s_theme)
        self.add_widget(self.s_lang)


class InfoCard(MD3Card):
    def init_ui(self):
        super(InfoCard, self).init_ui()
        self.title.text = 'Info:'


class UnitsCard(MD3Card):
    def init_ui(self):
        super(UnitsCard, self).init_ui()
        self.title.text = 'Units:'
        self.u_sh = SightHeightUnitSelector()
        self.u_tw = TwistUnitSelector()
        self.u_v = VelocityUnitSelector()
        self.u_dt = DistanceUnitSelector()
        self.u_t = TemperatureUnitSelector()
        self.u_w = WeightUnitSelector()
        self.u_ln = LengthUnitSelector()
        self.u_dm = DiameterUnitSelector()
        self.u_ps = PressureUnitSelector()
        self.u_ph = PathUnitSelector()
        self.u_a = AngularUnitSelector()
        self.u_dp = DropUnitSelector()
        self.u_e = EnergyUnitSelector()
        self.add_widget(self.u_sh)
        self.add_widget(self.u_tw)
        self.add_widget(self.u_v)
        self.add_widget(self.u_dt)
        self.add_widget(self.u_t)
        self.add_widget(self.u_w)
        self.add_widget(self.u_ln)
        self.add_widget(self.u_dm)
        self.add_widget(self.u_ps)
        self.add_widget(self.u_ph)
        self.add_widget(self.u_a)
        self.add_widget(self.u_dp)
        self.add_widget(self.u_e)


class InScrollBox(MDBoxLayout):
    pass


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.name = 'settings'
        self.init_ui()

    def init_ui(self):
        self.scroll = MDScrollView()
        self.layout = InScrollBox()

        self.view_card = ViewCard()
        self.unit_card = UnitsCard()
        self.info_card = InfoCard()

        self.layout.add_widget(self.view_card)
        self.layout.add_widget(self.unit_card)
        self.layout.add_widget(self.info_card)

        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)
