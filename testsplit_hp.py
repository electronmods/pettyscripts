#!/usr/bin/python3

from multiprocessing import Array, Lock, Process, Queue, Value
import sys
import time
from ctypes import c_bool

from pyubx2 import UBXReader
import pyubx2.ubxtypes_core as ubt
import pyubx2.exceptions as ube

def ubxsplit(q, iqueuedone):
    count = 0
    while (data := ubxsplitread()):
        count += 1
        q.put((count, data))
    with iqueuedone.get_lock():
        iqueuedone.value = True

def ubxsplitread():
    reading = True
    byte1 = stream.read(1)
    raw_data = None

    while reading:
        is_ubx = False
        is_nmea = False

        if len(byte1) < 1:  # EOF
            break
        if byte1 == ubt.UBX_HDR[0:1]:
            byte2 = stream.read(1)
            if len(byte2) < 1:  # EOF
                break
            if byte2 == ubt.UBX_HDR[1:2]:
                is_ubx = True
        if is_ubx:  # it's a UBX message
            byten = stream.read(4)
            if len(byten) < 4:  # EOF
                break
            clsid = byten[0:1]
            msgid = byten[1:2]
            lenb = byten[2:4]
            leni = int.from_bytes(lenb, "little", signed=False)
            byten = stream.read(leni + 2)
            if len(byten) < leni + 2:  # EOF
                break
            plb = byten[0:leni]
            cksum = byten[leni : leni + 2]
            raw_data = ubt.UBX_HDR + clsid + msgid + lenb + plb + cksum
            reading = False
        else:  # it's not a UBX message (NMEA or something else)
            prevbyte = byte1
            byte1 = stream.read(1)
            if prevbyte == b"\x24" and byte1 in (b"\x47", b"\x50"):  # "$G" or "$P"
                is_nmea = True  # looks like an NMEA message
    return raw_data

def ubxparse(iq, oq, procid, iqueuedone, oqueuedone):
    while iqueuedone.value is False or iq.empty() is False:
        try:
            curline, unparsed = iq.get()
        except:
            continue
        try:
            parsed = UBXReader.parse(unparsed)
        except ube.UBXParseError:
            parsed = None
        # while n.value != curline:
            # time.sleep(1e-8)
        # print(f'{curline}: {parsed}')
        oq.put((curline, parsed))
        # print(curline)
    with oqueuedone.get_lock():
        oqueuedone[procid] = True

def outputparsed(oq, oqueuedone):
    n = 1
    ordering = { }
    while True:
        if oq.empty() is False or all(oqueuedone) is False:
            curline, parsed = oq.get()
            ordering[curline] = parsed
        if n in ordering:
            r = str(ordering[n])
            if len(r) >= 80:
                print(f'{n}: {r[:80]}')
            else:
                print(f'{n}: {r}')
            del ordering[n]
            n += 1
        if oq.empty and all(oqueuedone) is True and ordering == { }:
            break

if __name__ == '__main__':
    numprocs = 18
    allprocs = []
    iqueuedone = Value(c_bool, False)
    oqueuedone = Array(c_bool, [False] * numprocs)
    pqueuedone = Value(c_bool)
    stream = open(sys.argv[1], 'rb', buffering=100000)
    inqueue = Queue(100)
    outqueue = Queue(100)

    allprocs.append(Process(target=ubxsplit, args=(inqueue, iqueuedone), daemon=True))
    for i in range(numprocs):
        allprocs.append(Process(target=ubxparse, args=(inqueue, outqueue, i, iqueuedone, oqueuedone), daemon=True))
    allprocs.append(Process(target=outputparsed, args=(outqueue, oqueuedone), daemon=True))
    for i in allprocs:
        i.start()
    for i in allprocs:
        i.join()
