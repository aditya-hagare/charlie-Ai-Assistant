from faster_whisper import WhisperModel

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def speech_to_text(audio_file="input.wav"):
    segments, info = model.transcribe(
        audio_file,
        beam_size=5,
        language=None,
        task="translate"
    )

    text = ""
    for segment in segments:
        text += segment.text

    return text.strip(), info.language
