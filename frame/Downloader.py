import json
import requests
from os import makedirs
from os.path import expanduser, isfile, dirname
import errno

CONFIG_FILE = expanduser("~/.config/pi-photo.config")

def get_config():
  if isfile(CONFIG_FILE):
    with open(CONFIG_FILE) as config:
      return json.load(config)
  else:
    return None

def fetch_files():
  try:
    cfg = get_config()
    if cfg is None:
      print("No config file, skipping download")
      return False
    index = requests.get(
      "{}/index.txt".format(cfg["url"]), 
      auth=(cfg['user'], cfg['pass'])
    )
    for file in index.text.rstrip().split('\n'):
      file = file.replace("..", "")
      target = "images/{}".format(file)
      if isfile(target):
        print("Skipping {}".format(file))
      else:
        print("Downloading {}".format(file))
        try:
          makedirs(dirname(target))
        except OSError as e:
          if e.errno != errno.EEXIST:
            raise
        with open(target, "wb") as output:
          image = requests.get(
            "{}/{}".format(cfg["url"], file), 
            auth=(cfg['user'], cfg['pass'])
          )
          for chunk in image.iter_content(chunk_size=128):
            output.write(chunk)
  except Exception as e:
    print("Error updating files: {}".format(e))
