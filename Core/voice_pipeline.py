from Core.audio import record_audio
from Core.speech_to_text import speech_to_text


def listen_command():
    audio_file = record_audio("input.wav")
    text, lang = speech_to_text(audio_file)

    print(f"Detected language: {lang}")
    print(f"Transcribed text: {text}")

    return text
