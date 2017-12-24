#!/usr/bin/env python3
# Talking to Google Maps Through a Bare Socket

import socket

# Use this to replace special characters in string using the %xx escape
from urllib.parse import quote_plus

# Request text
request_text = """\
GET /maps/api/geocode/json?address={}&sensor=false HTTP/1.1\r\n\
Host: maps.google.com:80\r\n\
User-Agent: search4.py (Foundations of Python Network Programming)\r\n\
Connection: close\r\n\
\r\n\
"""

def geocode(address):
    # Bottom layer, provided by host os to support basic networking over IP
    sock = socket.socket()
    sock.connect(('maps.google.com', 80))

    # Reformat request text
    request = request_text.format(quote_plus(address))

    # Send byte string over socket
    sock.sendall(request.encode('ascii'))

    # Another by string
    raw_reply = b''

    while True:
        more = sock.recv(4096)
        if not more:
            break
        raw_reply += more
    print(raw_reply.decode('utf-8'))
if __name__ == '__main__':
    geocode('207 N. Defiance St, Archbold, OH')
