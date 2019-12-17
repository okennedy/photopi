import kivy
from kivy.app import App
from kivy.config import Config
from kivy.clock import Clock
from frame import PhotoFrame

kivy.require('1.11.0') 
Config.read("config.ini")

class PhotoFrameApp(App):
    def build(self):
        photo = PhotoFrame()
        photo.refresh_images(None)
        Clock.schedule_interval(photo.step_forward, 60.0)
        return photo

if __name__ == '__main__':
    PhotoFrameApp().run()
