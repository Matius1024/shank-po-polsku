"""Wyciaga nagrania z banku FMOD FSB4 (data-pc\\bootstrap\\sound\\*.fsb) do plikow .wav.

Uzycie: python fsb_extract.py <plik.fsb> <folder wyjsciowy> [fragment nazwy ...]
Bez fragmentow tylko wypisuje liste nagran. Obsluguje PCM16, IMA ADPCM i MPEG (ffmpeg dekoduje MPEG do wav).
"""
import os
import struct
import subprocess
import sys

MODE_PCM16 = 0x10
MODE_MPEG = 0x200
MODE_IMAADPCM = 0x400000
FSB_SOURCE_FORMAT = 0x400  # w trybie banku: dane w formacie zrodlowym


def samples(path):
    with open(path, "rb") as f:
        d = f.read()
    if d[:4] != b"FSB4":
        raise ValueError("to nie FSB4")
    n, shdr, datasize, ver, mode = struct.unpack_from("<IIIII", d, 4)
    o = 48
    data = 48 + shdr
    out = []
    for _ in range(n):
        size = struct.unpack_from("<H", d, o)[0]
        name = d[o + 2:o + 32].split(b"\0")[0].decode("latin-1")
        length, csize, ls, le, smode, freq = struct.unpack_from("<IIIIII", d, o + 32)
        chans = struct.unpack_from("<H", d, o + 62)[0]
        out.append(dict(name=name, length=length, size=csize, mode=smode, freq=freq, chans=chans,
                        data=d[data:data + csize]))
        data += csize
        data = 48 + shdr + (data - 48 - shdr + 31) // 32 * 32  # dane kazdego nagrania zaczynaja sie co 32 bajty
        o += size
    return out


def to_wav(s, dst):
    if s["mode"] & MODE_MPEG:
        tmp = dst + ".mp3"
        with open(tmp, "wb") as f:
            f.write(s["data"])
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, dst], check=True)
        os.remove(tmp)
    elif s["mode"] & MODE_IMAADPCM:
        # Xbox/FMOD IMA ADPCM: 36 bajtow na blok i kanal; ffmpeg zna go jako adpcm_ima_wav w kontenerze wav
        block = 36 * s["chans"]
        fmt = struct.pack("<HHIIHHHH", 0x11, s["chans"], s["freq"], s["freq"] * block // 64, block, 4, 2, 64)
        riff = b"RIFF" + struct.pack("<I", 4 + 8 + len(fmt) + 8 + len(s["data"])) + b"WAVE"
        riff += b"fmt " + struct.pack("<I", len(fmt)) + fmt + b"data" + struct.pack("<I", len(s["data"])) + s["data"]
        tmp = dst + ".ima.wav"
        with open(tmp, "wb") as f:
            f.write(riff)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, dst], check=True)
        os.remove(tmp)
    else:
        import wave
        with wave.open(dst, "wb") as w:
            w.setnchannels(s["chans"])
            w.setsampwidth(2)
            w.setframerate(s["freq"])
            w.writeframes(s["data"])


def main():
    path, out = sys.argv[1], sys.argv[2]
    parts = [p.lower() for p in sys.argv[3:]]
    for s in samples(path):
        if not parts:
            print(f"{s['name']:32s} {s['freq']} Hz {s['chans']} kan. tryb {s['mode']:#x} {s['length'] / s['freq']:.1f} s")
        elif any(p in s["name"].lower() for p in parts):
            os.makedirs(out, exist_ok=True)
            dst = os.path.join(out, os.path.splitext(s["name"])[0] + ".wav")
            to_wav(s, dst)
            print("->", dst)


if __name__ == "__main__":
    main()
