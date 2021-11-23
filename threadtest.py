#!/usr/bin/python3

import hashlib
import logging
import random
import regex as re
import queue
import threading
import time

class CSVThreader(threading.Thread):
    def __init__(self, iq):
        self.iq = iq
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        for i in range(1000):
            self.iq.put([i, str(i) * 25])
            time.sleep(random.random()/100)

class GCThreader(threading.Thread):
    def __init__(self, iq, oq):
        self.iq = iq
        self.oq = oq
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        while True:
            csvid, csvstr = self.iq.get(timeout=2.0)
            print(csvstr)
            csvid *= -1
            tmpstr = re.compile('(' + r'\d' * (len(csvstr) // 25) + ')').findall(csvstr)
            self.oq.put([csvid, tmpstr])
            self.iq.task_done()

class CollectThreader(threading.Thread):
    def __init__(self, oq):
        self.oq = oq
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        while True:
            gcid, gcstr = self.oq.get(timeout=0.25)
            print(f'{gcid}: {gcstr}')
            self.oq.task_done()

num_gc_threads = 10
input_queue = queue.Queue(maxsize=5)
gc_outqueue = queue.Queue(maxsize=100)

csvthread = CSVThreader(input_queue)
csvthread.start()

gcthreads = [ ]
for i in range(num_gc_threads):
    gcthreads.append(GCThreader(input_queue, gc_outqueue))
for t in gcthreads: t.start()

printthread = CollectThreader(gc_outqueue)
printthread.start()

csvthread.join()
for t in gcthreads:
    t.join()
printthread.join()
