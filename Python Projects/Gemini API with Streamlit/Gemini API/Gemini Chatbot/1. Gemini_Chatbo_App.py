import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get API key (NEVER write directly in code)
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)

# Load model
model = genai.GenerativeModel("gemini-3-flash-preview")

# UI
st.title("Gemini Chatbot App")

# Input box
question = st.text_input("Enter your question:")

# Button
if st.button("Ask Gemini"):
    if question.strip() == "":
        st.warning("Please type a question first!")
    else:
        with st.spinner("Thinking... "):
            response = model.generate_content(question)
            st.markdown("### Answer:")
            st.markdown(response.text)