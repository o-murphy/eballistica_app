from kivymd.uix.toolbar import MDBottomAppBar
from kivy.lang import Builder


Builder.load_string("""
#:import MDActionBottomAppBarButton kivymd.uix.toolbar.MDActionBottomAppBarButton


<AppBottomBar>
    # md_bg_color: "#191c1a"
    # icon_color: "#8a938c"
    elevation: 3

    action_items:
        [
        MDActionBottomAppBarButton(icon='arrow-left', on_release=app.on_bottom_action_buttons)
        ]

    MDFabBottomAppBarButton:
        # md_bg_color: "#1f352a"
        left_action_items: [["coffee"]]
        icon: "plus"
        # icon_color: "#8a938c"
        elevation: 4
        on_release: app.add_act()
""")


class AppBottomBar(MDBottomAppBar):
    pass
