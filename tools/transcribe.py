"""Rozpisuje angielskie dialogi ze scenek (WAV) na pliki JSON z czasami kwestii.

Uzycie: python transcribe.py <folder wav> <folder wyjsciowy>
"""
import json
import os
import sys
import wave

import numpy

# Biblioteki CUDA z pakietow pip (nvidia-cublas-cu12, nvidia-cudnn-cu12) musza byc widoczne dla ctranslate2.
try:
    import nvidia.cublas, nvidia.cudnn
    for mod in (nvidia.cublas, nvidia.cudnn):
        os.add_dll_directory(os.path.join(list(mod.__path__)[0], "bin"))
        os.environ["PATH"] = os.path.join(list(mod.__path__)[0], "bin") + os.pathsep + os.environ["PATH"]
except ImportError:
    pass

from faster_whisper import WhisperModel


def main():
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    try:
        model = WhisperModel("large-v3", device="cuda", compute_type="float16")
    except Exception as e:
        print("GPU niedostepne, uzywam CPU:", e)
        model = WhisperModel("large-v3", device="cpu", compute_type="int8")
    for fn in sorted(os.listdir(src)):
        if not fn.endswith(".wav"):
            continue
        out = os.path.join(dst, fn[:-8] + ".json")
        if os.path.exists(out):
            continue
        with wave.open(os.path.join(src, fn), "rb") as w:
            audio = numpy.frombuffer(w.readframes(w.getnframes()), numpy.int16).astype(numpy.float32) / 32768
        segments, info = model.transcribe(
            audio, language="en", vad_filter=True,
            condition_on_previous_text=False, beam_size=5)
        lines = [{"start": round(s.start, 2), "end": round(s.end, 2), "en": s.text.strip()}
                 for s in segments]
        with open(out, "w", encoding="utf-8") as f:
            json.dump({"movie": fn[:-8], "duration": round(info.duration, 2), "lines": lines},
                      f, ensure_ascii=False, indent=1)
        print(fn, len(lines), flush=True)


if __name__ == "__main__":
    main()
