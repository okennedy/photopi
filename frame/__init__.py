from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.properties import BooleanProperty, ListProperty, NumericProperty
from glob import glob
from frame.settings import FrameSettings
from random import shuffle

class ImageButton(ButtonBehavior, Image):
  pass

Builder.load_file("frame/PhotoFrame.kv")

class PhotoFrame(Widget):
  images = ListProperty(["default.jpg"])
  index = NumericProperty(0)
  show_controls = BooleanProperty(False)
  show_settings = BooleanProperty(False)

  def __init__(self, **kvargs):
    super(PhotoFrame, self).__init__(**kvargs)

  def toggle_controls(self, touch = None):
    self.show_controls = not self.show_controls
    return True;

  def toggle_settings(self, touch = None):
    self.show_settings = not self.show_settings
    return True;

  def hide_ui(self, event = None):
    self.show_settings = False
    self.show_controls = False

  def reset_index(self, event, v):
    self.index = 0

  def step_forward(self, event = None):
    print("Forward")
    self.index = (self.index + 1) % len(self.images)
    return True

  def step_backward(self, event = None):
    print("Backward")
    self.index = (self.index - 1) % len(self.images)
    return True

  def refresh_images(self, event):
    self.index = 0
    images = glob("images/*.jpg") + glob("images/**/*.jpg")
    shuffle(images)
    self.images = images
