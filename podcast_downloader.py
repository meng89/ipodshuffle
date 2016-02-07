#!/usr/bin/env python3

import sys
import feedparser
import socket
timeout = 120
socket.setdefaulttimeout(timeout)

# feed_name = sys.argv[1]

feed_url = sys.argv[1]
d = feedparser.parse(feed_url.encode())

print(d)

for s in d.entries:
    print(s.title.decode(), s.link.decode())
