# cpyinaturalist
CircuitPython library for the iNaturalist API

## What is this?

This is a library to managing the iNaturalist API for CircuitPython 6. It is intended to be compatible with [niconoe Pyinaturalist](https://github.com/niconoe/pyinaturalist), but it is not yet.

## Compatible boards

So far, I only have working esp32s2 boards like the Funhouse, and I am working on adding boards like the PyPortal if possible.

## Install

```
circup install adafruit_imageload adafruit_requests adafruit_portalbase 
cp cpyinaturalist.py /media/$USER/CIRCUITPY # Example for Gnu/Linux
```

## Examples

Go to ``examples`` and find a code.py compatible with Adafruit Funhouse.

![Funhouse example](doc/imgs/funhouse.jpg)

## What can you do?

So far:

- Get a list of observations by running:

```
observations = Cpyinaturalist.get_observations(inat, user_id='fedecrc')
```

- Download an image from an observation:

```
Cpyinaturalist.get_image(inat, result["photos"][0]["small_url"])
```

*Note: This requires the board to be able to write to the internal memory. For this you need to unplug usb data*
