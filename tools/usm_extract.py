"""Wyciaga z filmow CRI .usm dzwiek (@SFA: ADX/HCA) i obraz (@SFV: strumien MPEG) do osobnych plikow.

Uzycie: python -I usm_extract.py <folder wyjsciowy> <plik.usm albo folder> [...]
Wynik: <wyjscie>/raw/<film>_ch<n>.adx i <wyjscie>/video/<film>.m2v
"""
import os
import struct
import sys


def extract(path, out_dir):
    name = os.path.splitext(os.path.basename(path))[0]
    audio, video = {}, bytearray()
    with open(path, "rb") as f:
        data = f.read()
    pos = 0
    while pos + 0x20 <= len(data):
        sig = data[pos:pos + 4]
        size = struct.unpack(">I", data[pos + 4:pos + 8])[0]
        if sig in (b"@SFA", b"@SFV"):
            hdr = pos + 8
            offset = data[hdr + 1]
            padding = struct.unpack(">H", data[hdr + 2:hdr + 4])[0]
            channel = data[hdr + 4]
            if data[hdr + 7] & 3 == 0:
                payload = data[hdr + offset:hdr + size - padding]
                if sig == b"@SFA":
                    audio.setdefault(channel, bytearray()).extend(payload)
                elif channel == 0:
                    video.extend(payload)
        pos += 8 + size
    written = []
    os.makedirs(os.path.join(out_dir, "raw"), exist_ok=True)
    os.makedirs(os.path.join(out_dir, "video"), exist_ok=True)
    for ch, buf in audio.items():
        ext = ".hca" if buf[:3] in (b"HCA", b"\xc8\xc3\xc1") else ".adx"
        out = os.path.join(out_dir, "raw", f"{name}_ch{ch}{ext}")
        with open(out, "wb") as o:
            o.write(buf)
        written.append(out)
    if video:
        out = os.path.join(out_dir, "video", name + ".m2v")
        with open(out, "wb") as o:
            o.write(video)
        written.append(out)
    return written


def main():
    dst = sys.argv[1]
    for src in sys.argv[2:]:
        files = [src] if os.path.isfile(src) else [os.path.join(src, f) for f in sorted(os.listdir(src))]
        for fn in files:
            if fn.lower().endswith(".usm"):
                for out in extract(fn, dst):
                    print(out)


if __name__ == "__main__":
    main()
