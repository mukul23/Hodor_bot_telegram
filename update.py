import urllib
import json

import connect

class Connect():
    def __init__(self, call_url):
        r = urllib.urlopen(call_url)
        response = json.loads(r)
