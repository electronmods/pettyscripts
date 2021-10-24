#!/usr/bin/python3

import subprocess as sp
import os
import sys

f = open('test_b2.bz2', 'wb')

p0 = sp.Popen(('/usr/bin/bzcat', 'test_a.bz2'), stdout=sp.PIPE, stderr=sp.DEVNULL)
p1 = sp.Popen(('/usr/bin/grep', '-v', '-E', '[[:digit:]]'), stdin=p0.stdout, stdout=sp.PIPE, stderr=sp.DEVNULL)
p2 = sp.Popen(('/usr/bin/bzip2', '-9c'), stdin=p1.stdout, stdout=f, stderr=sp.DEVNULL)
#p1.communicate()
#p0.stdout.close()
p0.wait()
