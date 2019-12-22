import kivy
kivy.require('1.11.0') 
from kivy.config import Config
Config.read("config.ini")
from kivy.app import App
from kivy.clock import Clock
from frame import PhotoFrame
from frame.Downloader import fetch_files
from frame.WiFi import WiFiSettings

class PhotoFrameApp(App):
  def build(self):
#    photo = WiFiSettings()
    photo = PhotoFrame()
    photo.refresh_images(None)
    Clock.schedule_interval(photo.step_forward, 60.0)
    Clock.schedule_interval(fetch_files, 60.0*60.0*24)
    return photo

if __name__ == '__main__':
    PhotoFrameApp().run()
