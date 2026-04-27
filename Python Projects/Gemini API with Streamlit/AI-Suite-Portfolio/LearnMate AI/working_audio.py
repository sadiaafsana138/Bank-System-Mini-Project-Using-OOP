from gtts import gTTS
import io

def text_to_audio(text, lang="en"):

    speech = gTTS(text=text, lang=lang, slow=False)

    audio_buffer = io.BytesIO()
    speech.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    return audio_buffer