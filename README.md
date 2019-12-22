## Pi Frame

A really really really simple digital photo frame script for a raspberry pi connected to a display
based on Kivy.  It's especially designed for use with a touch screen.


#### Instructions

1. Set up the raspberry pi with Raspbian Lite.  Configure it to boot to console.
2. Get the repository
3. Run `scripts/setup.sh`
4. Put a bunch of images into `images`.  Subdirectories are ok.
5. Run python3 main.py

#### Features

###### Wifi Configuration

Tap the screen and then tap the WiFi logo.  You'll see a list of available networks and an entry
field for adding new networks.

###### Automatic Downloading

Add a file `~/config/pi-photo.config` that looks like

```
{
  "url" : "<server url>",
  "user" : "<basic auth user>",
  "pass" : "<basic auth password>"
}
```

The album will periodically connect to `<server url>/index.txt`, expecting a list of file paths 
relative to `<server url>`.  If any of the files in that list have not already downloaded, they will
be downloaded.  If the downloader config is not present, it will be skipped.

#### Credits

Images used under public domain license from [freesvg.org](https://freesvg.org/).