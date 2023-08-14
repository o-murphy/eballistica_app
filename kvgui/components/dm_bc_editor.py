from kivy.uix.screenmanager import Screen

from kivy.lang import Builder

from kvgui.components.mixines import MapIdsMixine
from kvgui.modules.translator import translate as tr
from kvgui.modules import signals as sig

helper = """
<BCEditor>
    MDScrollView:
        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: "20dp"
            spacing: "15dp"
            
            MD3CardAbs:
                orientation: 'vertical'
                size_hint_y: None
                height: dp(320)
    
                MDLabel:
                    id: title
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    size_hint_x: 1
                    halign: 'center'
                    
                MDBoxLayout:
                    orientation: 'horizontal'
                    
                    MDLabel:
                        id: velocity_label
                        # pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                        size_hint_x: 0.5
                        halign: 'center'
                        
                    MDLabel:
                        id: bc_label
                        # pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                        size_hint_x: 0.5
                        halign: 'center'
                        
"""


Builder.load_file('kvgui/kv/dm_bc_editor.kv')
Builder.load_string(helper)


class BCEditor(Screen, MapIdsMixine):
    def __init__(self, **kwargs):
        super(BCEditor, self).__init__(**kwargs)
        self.name = 'bc_editor_screen'
        self.init_ui()
        self.bind_ui()

    def on_pre_enter(self, *args):  # Note: Definition that may translate ui automatically
        self.translate_ui()

    def init_ui(self):
        super(BCEditor, self).init_ui()
        self.translate_ui()

    def bind_ui(self):
        ...

    def translate_ui(self):
        self.title.text = tr('Edit BC: ', 'BCEditor') + ''  # Todo: display Drag Model
        self.velocity_label.text = tr('Velocity, ', 'BCEditor') + '{DragModel}'  # Todo: display Drag Model
        self.bc_label.text = tr('BC, ', 'BCEditor') + '{DragModel}'  # Todo: display Drag Model
