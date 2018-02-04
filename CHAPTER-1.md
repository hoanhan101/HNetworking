## Chapter 1: Client-Server Networking

**Goal:**
Find a longtitude and latitude of a given physical address.

### Stack and Library

**Solution 1:** Use a Python library *pygeocoder*.

```python

from pygeocoder import Geocoder

if __name__ == '__main__':
    # Save our target in a variable
    address = '207 N. Defiance St, Archbold, OH'

    # Print the answer
    print(Geocoder.geocode(address)[0].coordinates)
```

### Application Layers

**Solution 2:** Instead of using *pygeocoder*, drop down one level and use *requests*.

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

**Solution 3:** Use HTTP to fetch the result directly.

Making a Raw HTTP Connection to Google Maps.
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

### A Raw Network Converstaion

HTTP Protocol uses the capacity of modern operating systems to support a plain-text network conversation between two different programs across an IP network by using the TCP protocol.
In other words, it operates by dictating exactly what the text of the messages will look like that pass back and forth between two hosts that can speak TCP.

**Solution 4:** Talking to Google Maps Through a Bare Socket

```python

# Bottom layer: raw socket 
# Provided by by the host OS to support basic communications on an IP network
import socket

# Use this to replace special characters in string using the %xx escape
from urllib.parse import quote_plus

# HTTP request:
#   GET request, path of the document, and version of HTTP we support
#   A series of headers that each consist of a name, a colon, a value, \r\n
request_text = """\
GET /maps/api/geocode/json?address={}&sensor=false HTTP/1.1\r\n\
Host: maps.google.com:80\r\n\
User-Agent: search4.py (Foundations of Python Network Programming)\r\n\
Connection: close\r\n\
\r\n\
"""

def geocode(address):
    # Open a socket connection
    sock = socket.socket()

    # Connect to google maps on port 80
    sock.connect(('maps.google.com', 80))

    # Format out request
    request = request_text.format(quote_plus(address))

    # Send byte strings
    sock.sendall(request.encode('ascii'))

    raw_reply = b''
    while True:
        more = sock.recv(4096)
        if not more:
            break
        raw_reply += more

    # Decode the string and print it
    print(raw_reply.decode('utf-8'))

if __name__ == '__main__':
    geocode('207 N. Defiance St, Archbold, OH')
```

Output:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Date: Sat, 23 Nov 2013 18:34:30 GMT
Expires: Sun, 24 Nov 2013 18:34:30 GMT
Cache-Control: public, max-age=86400
Vary: Accept-Language
Access-Control-Allow-Origin: *
Server: mafe
X-XSS-Protection: 1; mode=block
X-Frame-Options: SAMEORIGIN
Alternate-Protocol: 80:quic
Connection: close
{
   "results" : [
{
...
         "formatted_address" : "207 North Defiance Street, Archbold, OH 43502, USA",
         "geometry" : {
            "location" : {
               "lat" : 41.521954,
               "lng" : -84.306691
},
... },
         "types" : [ "street_address" ]
      }
],
   "status" : "OK"
}
```

### IP Addresses

Turning a Hostname into an IP Address
```python

import socket

if __name__ == '__main__':
    hostname = 'www.python.org'
    addr = socket.gethostbyname(hostname)
    print('The IP address of {} is {}'.format(hostname, addr))
```

**Ranges:**
- `127.*.*.*`: reserved range that is local to the machine 
- `10.*.*.*, 172.16–31.*.*, 192.168.*.*`: private subnets

### Routing
- `127.0.0.0/8`: first 8-bit must match 127
- `192.168.0.0/16`: first 16-bit must match perfectly
- `192.168.5.0/24`: individual subnet

### Packet Fragmentation
IP supports maximum 64KB packet but actual network devices are built usually support much small packet size.

Internet packet include a 'Don't Fragment' (DF) flag for the user to decide if the packet is too big.
- If DF unset, it will be split into small packets and reassembled at the end
- If DF is set, it will be discarded and an error message will be sent back

For UDP, DF is unset. For TCP, DF is set.
