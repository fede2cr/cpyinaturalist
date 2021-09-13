import adafruit_imageload
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
import adafruit_requests
import board
import displayio
import time
import socketpool
import ssl
import wifi

import secrets
from cpyinaturalist import *

display = board.DISPLAY

font = bitmap_font.load_font("/fonts/ter-u12n.bdf")
font.load_glyphs(b'abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890- ()')


try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print("Connecting to ", secrets["ssid"])
wifi.radio.connect(ssid=secrets["ssid"], password=secrets["password"])
print("Connected with IP ", wifi.radio.ipv4_address)

inat = Cpyinaturalist()

#observations = Cpyinaturalist.get_observations(inat, user_id='fedecrc')
#observations = Cpyinaturalist.get_observations(inat)
observations = Cpyinaturalist.get_observations(inat, project='parque-nacional-isla-del-coco')
for result in observations:
    print(result["id"], result["observed_on"], result["species_guess"] )
    print(result)
    Cpyinaturalist.get_image(inat, result["photos"][0]["small_url"])
    bitmap, palette = adafruit_imageload.load("/inat.bmp",
                                          bitmap=displayio.Bitmap,
                                          palette=displayio.Palette)
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
    group = displayio.Group()
    group.append(tile_grid)
    display.show(group)
    time.sleep(10)
    print("Adding labels...")
    species_label = Label(font, text="Species: " + result["species_guess"], color=0x000000)
    species_label.x = 10
    species_label.y = 200
    group.append(species_label)
    author_label = Label(font, text="Author: " + result["user"]["login"], color=0x000000)
    author_label.x = 10
    author_label.y = 215
    group.append(author_label)
    date_label = Label(font, text="Observed in: " + result["observed_on"], color=0x000000)
    date_label.x = 10
    date_label.y = 230
    group.append(date_label)
    display.show(group)
    time.sleep(10)
