#!/usr/bin/python3

import io
import random
import string

ofb = io.open('foo.txt', 'w', buffering=int(1e6))

chars = string.ascii_letters + string.digits

for _ in range(int(1e5)):
    l = random.randint(20,150)
    strout = ''.join(random.choices(chars, k=l)) + '\n'
    ofb.write(strout)
