import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# API KEY
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3-flash-preview")


def analyze_image(image, mode):

    if mode == "Debug":
        prompt = """
        You are a coding assistant.
        Find the bug in the image/code.
        Explain clearly in simple words.
        """

    elif mode == "Hint":
        prompt = """
        Give ONLY a hint.
        Do NOT give full solution or code.
        """

    else:  # Solution
        prompt = """
        Give full corrected code.
        Explain what was wrong and how to fix it.
        """

    response = model.generate_content([image, prompt])

    return response.text
                