import pvporcupine
import pyaudio
import struct
import os
import sys

from Core.interrupt import clear_interrupt


# ================= RESOURCE PATH FIX =================

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


KEYWORD_PATH = resource_path("wake_words/hello_charlie.ppn")

ACCESS_KEY = "ywFRFPc4yzou9BeaKsvTgxTcApPhG6uBZs6YyMOxFviYD20zbqP2WA=="
SENSITIVITY = 0.8


def wait_for_wake_word():

    if not os.path.exists(KEYWORD_PATH):
        raise FileNotFoundError(f"Wake word file not found: {KEYWORD_PATH}")

    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=[KEYWORD_PATH],
        sensitivities=[SENSITIVITY]
    )

    pa = pyaudio.PyAudio()

    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("🤖 CHARLIE sleeping... say 'Hello Charlie'")

    try:
        while True:
            pcm = stream.read(
                porcupine.frame_length,
                exception_on_overflow=False
            )

            pcm = struct.unpack_from(
                "h" * porcupine.frame_length,
                pcm
            )

            result = porcupine.process(pcm)

            if result >= 0:
                print("⚡ Wake word detected!")
                clear_interrupt()
                return

    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()
