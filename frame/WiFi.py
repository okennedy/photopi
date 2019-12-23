from lib.wpa_supplicant import WPASupplicant
import threading
import time
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView

# Based on instructions from the wpa_supplicant PyPi install readme and project page: 
# - https://pypi.org/project/wpa_supplicant/
# - https://digidotcom.github.io/python-wpa-supplicant/0.2/api.html


Builder.load_file("frame/WiFi.kv")

class WiFiSettings(BoxLayout):
  networks = ListProperty()
  active_connection = ObjectProperty(None)
  new_network_ssid = ObjectProperty()
  new_network_password = ObjectProperty()
  visible = BooleanProperty(False)

  def __init__(self, **kvargs):
    super(WiFiSettings, self).__init__(**kvargs)
    self.supplicant = WPASupplicant()
    self.register_event_type("on_done")
    self.start_network_refresh()
    Clock.schedule_interval(self.start_network_refresh, 60*2)

  def start_network_refresh(self, event = None):
    try:
      self.supplicant.command("scan")
      Clock.schedule_once(self.reload_networks, 10)
    except e as Exception:
      print("Error refreshing networks: {}".format(e))


  def reload_networks(self, event = None):
    try:
      self.command("scan_results")
      Clock.schedule_once(self.finish_reload, 1)
    except e as Exception:
      print("Error refreshing networks: {}".format(e))

  def finish_reload(self, event = None):
    try:
      print([
        { 
          "network" : net,
          "ssid" : net.ssid
        }
        for net in supplicant.networks:
      ])
    except e as Exception:
      print("Error refreshing networks: {}".format(e))




  def handle_connect(self):
    conf = {
      "scan_ssid" : 1,
      "ssid" : self.new_network_ssid.text,
      "psk" : self.new_network_password.text
    }
    self.interface.add_network(conf)
#    print("CONNECT: {}".format(conf))

  def handle_done(self, event = None):
    self.dispatch("on_done", event)

  def on_done(self, event = None):
    print("DONE")

class WiFiNetworkList(RecycleView):
  pass

class WiFiNetwork(BoxLayout):
  ssid = StringProperty()
  network = ObjectProperty()
  connected = BooleanProperty(True)

  def __init__(self, **kvargs):
    super(WiFiNetwork, self).__init__(**kvargs)

  def handle_delete(self, event = None):
    print("Should Delete: {}".format(network))
