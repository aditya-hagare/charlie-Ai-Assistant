import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import time

SAMPLE_RATE = 16000
SILENCE_THRESHOLD = 0.01
MAX_SILENCE_SEC = 3
MAX_RECORD_SEC = 15


def record_audio(filename="input.wav"):
    print("🎤 Speak now...")

    frames = []
    silence_time = 0.0
    start_time = time.time()

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        blocksize=1024
    ) as stream:
        while True:
            data, _ = stream.read(1024)
            frames.append(data.copy())

            rms = np.sqrt(np.mean(data ** 2))

            if rms < SILENCE_THRESHOLD:
                silence_time += 1024 / SAMPLE_RATE
            else:
                silence_time = 0.0

            if silence_time >= MAX_SILENCE_SEC:
                break

            if time.time() - start_time > MAX_RECORD_SEC:
                break

    audio = np.concatenate(frames, axis=0)
    audio_int16 = np.int16(audio * 32767)
    write(filename, SAMPLE_RATE, audio_int16)

    return filename
