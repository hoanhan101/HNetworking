# python network programming
The goal of this project is to acquire a deeper understanding of network programming in Python.
It follows the book [Foundations of Python Network Programming book, Third 
Edition by Brandon Rhodes, John Goerzen](https://github.com/brandon-rhodes/fopnp).

The source code for the book is avaiable online at 
[https://github.com/brandon-rhodes/fopnp/tree/m/py3](https://github.com/brandon-rhodes/fopnp/tree/m/py3).

This is a setup with Docker that provides a sample network of 12 machines:
[https://github.com/brandon-rhodes/fopnp/tree/m/playground](https://github.com/brandon-rhodes/fopnp/tree/m/playground).

Notes are made by me.

## Chapter 1: Client-Server Networking

**Why using `virtualenv`:**
It allows us to create a virutal environment where we can experiment installing/uninstalling
packages without contaminating your systemwide Python.

**How to use `virtualenv` for a project once it get installed:**
- `virtualenv –p python3 env_name` to create a virutal environment where `env_name` is your environment/directory name.
- `cd env_name`
- `. bin/activate`
- Now you are inside your virtual environment, install dependency as normal: `pip install module_name`.
- Import module: `python -c 'import module_name'`.

### Stack and Library

**Goal:**
Find a longtitude and latitude of a given physical address.

**Solution 1:** 
Use a Python library *pygeocoder*.
```python

from pygeocoder import Geocoder
if __name__ == '__main__':
    address = '207 N. Defiance St, Archbold, OH'
    print(Geocoder.geocode(address)[0].coordinates)
```

### Application Layers

**Solution 2:**
Instead of using *pygeocoder*, drop down one level and use *requests*.

Use Google Geocoding API to fetch a JSON document.
```python

import requests
def geocode(address):
    parameters = {'address': address, 'sensor': 'false'}
    base = 'http://maps.googleapis.com/maps/api/geocode/json'
    response = requests.get(base, params=parameters)
    answer = response.json()
    print(answer['results'][0]['geometry']['location'])

if __name__ == '__main__':
    geocode('207 N. Defiance St, Archbold, OH')
```

### Speaking a Protocol
The second solution works because it creates a URL and fetches the document that corresponding to it.
The URL provides instructions that tell a lower level protocol, Hypertext Transfer Protocol (HTTP), how to find the document.
It consists:
- the name of a protocol
- the name of the machine where the document lives
- the path of that document.

**Solution 3:**
Use HTTP to fetch the result directly.
```python

import http.client
import json
from urllib.parse import quote_plus
base = '/maps/api/geocode/json'

def geocode(address):
    # Contruct query parameters
    path = '{}?address={}&sensor=false'.format(base, quote_plus(address))

    # Connect to a specific machine
    connection = http.client.HTTPConnection('maps.google.com')

    # Issue a GET request with a constructed path
    connection.request('GET', path)

    # Read the reply directly from the HTTP connection
    rawreply = connection.getresponse().read()

    # Load to JSON
    reply = json.loads(rawreply.decode('utf-8'))
    print(reply['results'][0]['geometry']['location'])

if __name__ == '__main__':
    geocode('207 N. Defiance St, Archbold, OH')
```
