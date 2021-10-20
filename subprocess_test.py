#!/usr/bin/python

import io
import os
import shutil
import subprocess as sp
import sys

ls_cmd = shutil.which('ls')
gzip_cmd = shutil.which('gzip')

f = open('foo.gz', 'wb')

p0 = sp.Popen((ls_cmd, '-Rl', '/etc'), stdout=sp.PIPE, stderr=sp.DEVNULL, bufsize=4)
p1 = sp.Popen((gzip_cmd, '-9', '-'), stdin=p0.stdout, stdout=f)
p0.stdout.close()
