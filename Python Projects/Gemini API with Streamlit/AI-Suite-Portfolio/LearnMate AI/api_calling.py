from google import genai
from dotenv import load_dotenv
import os
import io
from gtts import gTTS

load_dotenv()

my_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=my_api_key)


# ---------------- NOTE GENERATOR ----------------
def note_generator(images, selected_language):

    language = "Bangla (Bengali)" if selected_language == "Bangla" else "English"

    prompt = f"""
    Summarize the pictures in clean note format in {language}.
    Max 200 words.
    Use markdown with headings and bullet points.
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=images + [prompt]
    )

    return response.text


# ---------------- AUDIO ----------------
def audio_transcription(text, language):

    lang_code = "bn" if language == "Bangla" else "en"

    speech = gTTS(text=text, lang=lang_code, slow=False)

    audio_buffer = io.BytesIO()
    speech.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    return audio_buffer


# ---------------- QUIZ GENERATOR ----------------
def quiz_generator(images, difficulty, language):

    lang = "Bangla (Bengali)" if language == "Bangla" else "English"

    prompt = f"""
    Generate 3 MCQ quizzes in {lang}.
    Difficulty: {difficulty}

    Format STRICTLY like:

    Q: Question here
    A. option 1
    B. option 2
    C. option 3
    D. option 4
    Answer: A
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=images + [prompt]
    )

    return response.text