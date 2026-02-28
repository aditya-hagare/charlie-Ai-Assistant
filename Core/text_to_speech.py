import asyncio
import edge_tts
import sounddevice as sd
import soundfile as sf
import tempfile
import os
import threading

VOICE = "en-US-AriaNeural"

# Global state
speech_thread = None
stop_flag = threading.Event()
speech_lock = threading.Lock()


def stop_speaking():
    stop_flag.set()
    sd.stop()


async def _generate_and_play(text):
    global stop_flag

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        wav_path = f.name

    # Generate audio file
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(wav_path)

    if stop_flag.is_set():
        os.remove(wav_path)
        return

    data, samplerate = sf.read(wav_path)

    sd.play(data, samplerate)

    while sd.get_stream().active:
        if stop_flag.is_set():
            sd.stop()
            break
        await asyncio.sleep(0.05)

    sd.stop()
    os.remove(wav_path)


def _run_async(text):
    asyncio.run(_generate_and_play(text))


def speak(text: str):
    global speech_thread, stop_flag

    if not text:
        return

    with speech_lock:
        # Stop previous speech
        stop_flag.set()
        sd.stop()

        # Reset stop flag
        stop_flag = threading.Event()

        # Start new speech thread
        speech_thread = threading.Thread(
            target=_run_async,
            args=(text,),
            daemon=True
        )
        speech_thread.start()
