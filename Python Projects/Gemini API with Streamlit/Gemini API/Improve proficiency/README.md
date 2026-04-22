# Professional Sentence Improver

> A Streamlit web app powered by Google Gemini AI that rewrites your sentences in a professional tone.

🔗 **Live Demo:** [https://improve-proficiency.streamlit.app/](https://improve-proficiency.streamlit.app/)

---

## Features

- Enter any sentence and get a professionally rewritten version instantly
- Powered by Google Gemini (`gemini-2.0-flash-preview`)
- Clean and minimal Streamlit UI
- Secure API key loading via environment variables

---

## Tech Stack

- Python
- Streamlit
- Google Generative AI SDK (`google-generativeai`)
- python-dotenv

---

## Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/sadiaafsana138/ml_ai-projects.git
```

**2. Install dependencies**
```bash
pip install streamlit google-generativeai python-dotenv
```

**3. Set up your API key**

Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_api_key_here
```

**4. Run the app**
```bash
streamlit run app.py
```

---

## Project Structure

```
├── app.py               # Main Streamlit app
├── requirements.txt     # Python dependencies
├── .env                 # API key (not committed to Git)
├── .gitignore           # Excludes .env from version control
└── README.md            # Project documentation
```

---

## requirements.txt

```
streamlit
google-generativeai
python-dotenv
```

---

## Notes

- Never commit your `.env` file — add it to `.gitignore`
- Get your Gemini API key from [https://aistudio.google.com/](https://aistudio.google.com/)
- For Streamlit Cloud deployment, add `GOOGLE_API_KEY` in the app **Secrets** settings

---

## Author

Sadia Afsana — ML/AI Projects
