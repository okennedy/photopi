from wpa_supplicant.core import WpaSupplicantDriver, Interface
from twisted.internet.selectreactor import SelectReactor
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

  def __init__(self, **kvargs):
    super(WiFiSettings, self).__init__(**kvargs)
    self.reactor = SelectReactor()
    threading.Thread(
      target=self.reactor.run, 
      daemon=True,
      kwargs={'installSignalHandlers': 0}
    ).start()
    time.sleep(0.1)
    self.driver = WpaSupplicantDriver(self.reactor)
    self.supplicant = self.driver.connect()
    self.interface = Interface(self.supplicant.get_interfaces()[0], self.supplicant._conn, self.reactor)
    self.register_event_type("on_done")
    self.refresh_networks()
    Clock.schedule_interval(self.refresh_networks, 60*2)

  def refresh_networks(self, event = None):
    try:
      self.active_connection = self.interface.get_current_network()
      self.networks = self.interface.get_networks()
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
