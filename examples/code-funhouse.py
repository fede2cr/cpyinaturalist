import adafruit_imageload
import adafruit_requests
import board
import displayio
import time
import socketpool
import ssl
import wifi
from digitalio import DigitalInOut, Direction, Pull

from cpyinaturalist import *

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print("Connecting to ", secrets["ssid"])
wifi.radio.connect(ssid=secrets["ssid"], password=secrets["password"])
print("Connected with IP ", wifi.radio.ipv4_address)

inat = Cpyinaturalist()

observations = Cpyinaturalist.get_observations(inat, user_id='fedecrc')
for result in observations:
    print(result["id"], result["observed_on"], result["species_guess"] )
    Cpyinaturalist.get_image(inat, result["photos"][0]["small_url"])
    bitmap, palette = adafruit_imageload.load("/purple.bmp",
                                          bitmap=displayio.Bitmap,
                                          palette=displayio.Palette)
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
    group = displayio.Group()
    group.append(tile_grid)
    display.show(group)
    time.sleep(60)
