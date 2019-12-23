from subprocess import Popen, PIPE
import select
from threading import Thread
from time import sleep
import re

SUPPLICANT_CONFIG="/etc/wpa_supplicant/wpa_supplicant.conf"
SPLIT_LINE="#### DO NOT EDIT BELOW THIS LINE ####\n"

class Network:
  def __init__(self, mac, freq, level, flags, ssid = None):
    self.mac = mac
    self.freq = freq
    self.level = level
    self.flags = flags
    self.ssid = ssid

  def __repr__(self):
    return "{} @ {}dB ({}; {})".format(self.ssid, self.level, self.mac, self.flags)

class WPASupplicant:
  def __init__(self):
    self.cli = Popen(
      ["/sbin/wpa_cli"],
      # bufsize = 1,
      stdout = PIPE,
      stdin = PIPE
    )
    self.networks = {}
    for line in self.cli.stdout:
      line = line.decode().rstrip()
      if line == "Interactive mode":
        break
    self.listener = Thread(target = self.listen, daemon = True)
    self.listener.start()

  def command(self, command):
    self.cli.stdin.write("{}\n".format(command).encode())
    self.cli.stdin.flush()

  def scan(self, pause = 10):
    self.command("scan")
    sleep(pause)
    self.command("scan_results")
    sleep(0.5)

  def write_config(self, ssid, password):
    content = []
    with open(SUPPLICANT_CONFIG) as f:
      for line in f:
        if line == SPLIT_LINE:
          break
        content += [ line ]

    with open(SUPPLICANT_CONFIG, "w") as f:
      for line in content:
        f.write(line)
      f.write(SPLIT_LINE)
      f.write("network={\n")
      f.write('  scan_ssid=1\n')
      f.write('  ssid="{}"\n'.format(ssid))
      f.write('  psk="{}"\n'.format(password))
      f.write("}\n")
    self.command("reconfigure")


  def listen(self):
    for line in self.cli.stdout:
      line = line.decode().rstrip()
      print("---> {}".format(line))
      if(re.match("^[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}", line)):
        net = Network(*line.split("\t"))
        self.networks[net.ssid] = net
