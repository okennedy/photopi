from lib.wpa_supplicant import WPASupplicant
import threading
import time
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors.button import ButtonBehavior

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
    # self.networks = [{ 
    #   "network" : None,
    #   "ssid" : "TEST"
    # }]
    self.start_network_refresh()
    Clock.schedule_interval(self.start_network_refresh, 60*2)

  def start_network_refresh(self, event = None):
    try:
      self.supplicant.command("scan")
      Clock.schedule_once(self.reload_networks, 5)
    except Exception as e:
      print("Error refreshing networks: {}".format(e))


  def reload_networks(self, event = None):
    try:
      self.supplicant.command("scan_results")
      Clock.schedule_once(self.finish_reload, 1)
    except Exception as e:
      print("Error refreshing networks: {}".format(e))

  def finish_reload(self, event = None):
    try:
      print(self.supplicant.networks)
      self.networks = [
        { 
          "network" : net,
          "ssid" : net.ssid,
          "supplicant" : self
        }
        for mac in self.supplicant.networks
        for net in [self.supplicant.networks[mac]]
        if net.ssid != None
      ]
      print(self.networks)
    except Exception as e:
      print("Error refreshing networks: {}".format(e))

  def handle_connect(self):
    self.supplicant.write_config(
      self.new_network_ssid.text,
      self.new_network_password.text
    )
    self.handle_done()
#    print("CONNECT: {}".format(conf))

  def handle_done(self, event = None):
    self.dispatch("on_done", event)

  def on_done(self, event = None):
    print("DONE")

  def select_network(self, network):
    self.new_network_ssid.text = network.ssid

class WiFiNetworkList(RecycleView):
  pass

class WiFiNetwork(ButtonBehavior, BoxLayout):
  ssid = StringProperty()
  network = ObjectProperty()
  supplicant = ObjectProperty()

  def __init__(self, **kvargs):
    super(WiFiNetwork, self).__init__(**kvargs)

  def on_release(self, event = None):
    print("Selected: {}".format(self.network))
    self.supplicant.select_network(self.network)
