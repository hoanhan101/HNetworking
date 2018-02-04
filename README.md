# python network programming
The goal of this project is to acquire a deeper understanding of network programming in Python.
It follows the book [Foundations of Python Network Programming book, Third Edition by Brandon Rhodes, John Goerzen](https://github.com/brandon-rhodes/fopnp).


Notes are made by me.

## Chapter 1: Client-Server Networking

**Goal:**
Find a longtitude and latitude of a given physical address.

### Stack and Library

**Solution 1:** 
Use a Python library *pygeocoder*.
```python

from pygeocoder import Geocoder

if __name__ == '__main__':
    # Save our target in a variable
    address = '207 N. Defiance St, Archbold, OH'

    # Print the answer
    print(Geocoder.geocode(address)[0].coordinates)
```

### Application Layers

**Solution 2:**
Instead of using *pygeocoder*, drop down one level and use *requests*.

Use Google Geocoding API to fetch a JSON document.
```python

import requests

def geocode(address):
    # Construct query parameters
    parameters = {'address': address, 'sensor': 'false'}

    # Base URL
    base = 'http://maps.googleapis.com/maps/api/geocode/json'

    # Issue a GET request
    response = requests.get(base, params=parameters)

    # Load the reponse in JSON
    answer = response.json()

    # Print the answer
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

    # Print the answer
    print(reply['results'][0]['geometry']['location'])

if __name__ == '__main__':
    geocode('207 N. Defiance St, Archbold, OH')
```
