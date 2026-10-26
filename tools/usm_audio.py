"""Wyciaga sciezke dzwiekowa (@SFA) z filmow CRI .usm do surowych plikow (ADX lub HCA).

Uzycie: python -I usm_audio.py <folder z .usm> <folder wyjsciowy>
"""
import os
import struct
import sys


def extract(path, out_dir):
    name = os.path.splitext(os.path.basename(path))[0]
    streams = {}
    with open(path, "rb") as f:
        data = f.read()
    pos = 0
    while pos + 0x20 <= len(data):
        sig = data[pos:pos + 4]
        size = struct.unpack(">I", data[pos + 4:pos + 8])[0]
        if sig == b"@SFA":
            hdr = pos + 8
            offset = data[hdr + 1]
            padding = struct.unpack(">H", data[hdr + 2:hdr + 4])[0]
            channel = data[hdr + 4]
            ctype = data[hdr + 7] & 3
            if ctype == 0:
                payload = data[hdr + offset:hdr + size - padding]
                streams.setdefault(channel, bytearray()).extend(payload)
        pos += 8 + size
    written = []
    for ch, buf in streams.items():
        ext = ".hca" if buf[:3] in (b"HCA", b"\xc8\xc3\xc1") else ".adx"
        out = os.path.join(out_dir, f"{name}_ch{ch}{ext}")
        with open(out, "wb") as o:
            o.write(buf)
        written.append(out)
    return written


def main():
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    for fn in sorted(os.listdir(src)):
        if fn.lower().endswith(".usm"):
            for out in extract(os.path.join(src, fn), dst):
                print(out)


if __name__ == "__main__":
    main()
