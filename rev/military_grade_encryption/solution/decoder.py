#!/usr/bin/python3
import base64

def unscramble (text):
    data = bytearray (base64.b64decode(text))
    for i in range (0, len(data) - 1, 2):
        data[i], data[i+1] = data[i+1], data[i]
        
    for i in range (len(data) - 1, 0, -1):
        data[i] = data[i] ^ data[i - 1]

    print (str(data))
