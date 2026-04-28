import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_image(image, mode):

    if mode == "Debug":
        prompt = """
        You are a coding assistant.
        Find the bug in this code/image.
        Explain the error clearly and simply.
        """

    elif mode == "Hint":
        prompt = """
        Give only a hint to fix the problem.
        Do NOT give full solution or code.
        """

    else:  # Solution
        prompt = """
        Give full corrected code.
        Explain what was wrong and how to fix it.
        """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[image, prompt]
    )

    return response.text