import adafruit_requests
import adafruit_imageload
import adafruit_portalbase.network
import board
import displayio
import json
import os
import ssl
import socketpool
import storage
import wifi
import time

import secrets

class Cpyinaturalist(object):
    '''
    Class for managing the inaturalist api
    '''
    def __init__(self):
        self.socket_pool = socketpool.SocketPool(wifi.radio)
        self.requests = adafruit_requests.Session(self.socket_pool, ssl.create_default_context())

    def get_observations(self, user_id=None, project=None, taxon_id=None, iconic_taxa=None, quality_grade=None):
        url_add = ''
        if user_id == project == taxon_id == iconic_taxa == quality_grade ==None:
            url = 'https://www.inaturalist.org/observations.json/'
        else:
            url = 'https://www.inaturalist.org/observations.json/?'
            if user_id != None:
                url_add=url_add + 'user_id=' + user_id
                url = url + url_add
            if project != None:
                url = 'https://www.inaturalist.org/observations/project/' + project + '.json'
        print(url)
        response = self.requests.get(url)
        result = json.loads(response.text)
        return(result)


    def wget(self, url, filename, *, chunk_size=12000):
        """Download a url and save to filename location, like the command wget.
        :param url: The URL from which to obtain the data.
        :param filename: The name of the file to save the data to.
        :param chunk_size: how much data to read/write at a time.
        """
        print("Fetching stream from", url)

        response = self.requests.get(url, stream=True)

        headers = {}
        for title, content in response.headers.items():
            headers[title.lower()] = content

        if response.status_code == 200:
            print("Reply is OK!")
        if "content-length" in headers:
            content_length = int(headers["content-length"])
        else:
            raise RuntimeError("Content-Length missing from headers")
        remaining = content_length
        print("Saving data to ", filename)
        stamp = time.monotonic()
        file = open(filename, "wb")
        for i in response.iter_content(min(remaining, chunk_size)):  # huge chunks!
            remaining -= len(i)
            file.write(i)
            if not remaining:
                break
        file.close()

        response.close()
        stamp = time.monotonic() - stamp
        print(
            "Created file of %d bytes in %0.1f seconds" % (os.stat(filename)[6], stamp)
        )
        if not content_length == os.stat(filename)[6]:
            raise RuntimeError

    def get_image(self, imgurl):
        print(secrets.secrets)
        conv_url = "https://io.adafruit.com/api/v2/"+secrets.secrets["aio_username"]+"/integrations/image-formatter?x-aio-key="+secrets.secrets["aio_key"]+"&width=240&height=240&output=BMP8&url="+imgurl
        print(conv_url)
        storage.remount("/", False)
        self.wget(conv_url, '/inat.bmp', chunk_size=4096)
        storage.remount("/", True)

