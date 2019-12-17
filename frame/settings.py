
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput

Builder.load_file("frame/FrameSettings.kv")

class FrameSettings(BoxLayout):
  wifi_ssid = StringProperty("ssid")
  wifi_password = StringProperty("password")

  def __init__(self, **kvargs):
    super(FrameSettings, self).__init__(**kvargs)
    self.register_event_type("on_save")

  def do_save(self, event = None):
    print("SAVE")
    self.dispatch("on_save", event)

  def on_save(self, event = None):
    print("DID SAVE")