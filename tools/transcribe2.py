"""Druga wersja rozpisywania: czyta sam glos (po oddzieleniu muzyki przez demucs), bez filtra ciszy.

Uzycie: python transcribe2.py <folder sep\\htdemucs> <folder wyjsciowy> [film ...]
"""
import json
import os
import subprocess
import sys

try:
    import nvidia.cublas, nvidia.cudnn
    for mod in (nvidia.cublas, nvidia.cudnn):
        d = os.path.join(list(mod.__path__)[0], "bin")
        os.add_dll_directory(d)
        os.environ["PATH"] = d + os.pathsep + os.environ["PATH"]
except ImportError:
    pass

import numpy
from faster_whisper import WhisperModel

PROMPT = ("Shank, Cesar, Ava, Angelo, Cassandra, Butcher, Denny, Rudy, Corazon, Father Gomez, El Raton, "
          "the cartel. Dialogue from a film.")


def load(path):
    pcm = subprocess.run(["ffmpeg", "-loglevel", "fatal", "-i", path, "-ar", "16000", "-ac", "1", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return numpy.frombuffer(pcm, numpy.int16).astype(numpy.float32) / 32768


def add_line(lines, words):
    if not words:
        return
    text = "".join(w.word for w in words).strip()
    p = sum(w.probability for w in words) / len(words)
    # Whisper zmysla "Thank you." w muzyce i powtarza podpowiedz; takie kwestie odrzucamy.
    if p < 0.4 or "Dialogue from a film" in text or (text == "Thank you." and p < 0.9):
        return
    lines.append({"start": round(words[0].start, 2), "end": round(words[-1].end, 2), "en": text, "p": round(p, 2)})


def main():
    src, dst = sys.argv[1], sys.argv[2]
    only = set(sys.argv[3:])
    os.makedirs(dst, exist_ok=True)
    model = WhisperModel("large-v3", device="cuda", compute_type="float16")
    for movie in sorted(os.listdir(src)):
        if only and movie not in only:
            continue
        audio = load(os.path.join(src, movie, "vocals.wav"))
        segments, info = model.transcribe(
            audio, language="en", vad_filter=False, beam_size=5, word_timestamps=True,
            condition_on_previous_text=False, initial_prompt=PROMPT,
            no_speech_threshold=0.5, log_prob_threshold=-1.0)
        lines = []
        for s in segments:
            # Dlugi fragment dzielony na zdania (koniec slowa na . ? !), zeby lektor wchodzil w dobrym momencie.
            sentence = []
            for w in s.words or []:
                if w.probability <= 0.15:
                    continue
                sentence.append(w)
                if w.word.strip()[-1:] in ".?!" or w is s.words[-1]:
                    add_line(lines, sentence)
                    sentence = []
            add_line(lines, sentence)
        with open(os.path.join(dst, movie + ".json"), "w", encoding="utf-8") as f:
            json.dump({"movie": movie, "duration": round(info.duration, 2), "lines": lines},
                      f, ensure_ascii=False, indent=1)
        print(movie, len(lines), flush=True)


if __name__ == "__main__":
    main()
