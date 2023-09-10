from modules.env import IS_ANDROID
from modules import signals as sig
from kivymd.toast import toast as kivy_toast


def toast(text='', duration=2.5, **kwargs):
    try:
        if IS_ANDROID:
            return kivy_toast(text=text, gravity=80, length_long=duration)
        else:
            kivy_toast(text=text, duration=duration)
    except Exception:
        kivy_toast(text=text)


sig.toast.connect(toast)
