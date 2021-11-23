#!/usr/bin/python3

from multiprocessing import Lock, Process, Queue, Value
import sys
import time

from pyubx2 import UBXReader
import pyubx2.ubxtypes_core as ubt
import pyubx2.exceptions as ube

def ubxsplit(q, c):
    while (data := ubxsplitread()):
        with c.get_lock():
            c.value += 1
        q.put((c.value, data))
    q.close()

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

def ubxparse(iq, oq, n):
    while True:
        curline, unparsed = iq.get()
        try:
            parsed = UBXReader.parse(unparsed)
        except ube.UBXParseError:
            parsed = None
        # while n.value != curline:
            # pass
        # print(f'{curline}: {parsed}')
        oq.put((curline, parsed))

def outputparsed(oq, n):
    while True:
        curline, parsed = oq.get()
        if parsed and parsed.identity == 'NAV-POSLLH': print(f'{curline}: {parsed}')
        with n.get_lock():
            n.value += 1

if __name__ == '__main__':
    # manager = Manager()
    # ns = manager.Namespace()
    count = Value('i', 0)
    nextup = Value('i', 1)
    numprocs = 4
    allprocs = []
    stream = open(sys.argv[1], 'rb', buffering=100000)
    inqueue = Queue(1)
    outqueue = Queue(1)

    allprocs.append(Process(target=ubxsplit, args=(inqueue, count), daemon=True))
    for i in range(numprocs):
        allprocs.append(Process(target=ubxparse, args=(inqueue, outqueue, nextup), daemon=True))
    allprocs.append(Process(target=outputparsed, args=(outqueue, nextup), daemon=True))
    for i in allprocs:
        i.start()
    for i in allprocs:
        i.join()


