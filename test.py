#!/usr/bin/env python3

chunk = open('/run/media/chenmeng/IPOD2/iPod_Control/iTunes/iTunesSD', 'rb').read()


length = int.from_bytes(chunk[8:13], byteorder='little')

print(length)
