import streamlit as st
from api_calling import note_generator, audio_transcription, quiz_generator
from PIL import Image

st.title("📚 AI Note + Quiz Generator")
st.markdown("Upload up to 3 images to generate notes & quizzes")
st.divider()

# ---------------- SESSION STATE ----------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []


# ---------------- QUIZ PARSER ----------------
def parse_quiz(text):
    questions = text.split("Q:")
    quiz_list = []

    for q in questions[1:]:
        try:
            parts = q.split("Answer:")
            question_part = parts[0].strip()
            answer = parts[1].strip()[0]

            lines = question_part.split("\n")
            question = lines[0].strip()
            options = [l.strip() for l in lines[1:] if l.strip()]

            quiz_list.append({
                "question": question,
                "options": options,
                "answer": answer
            })
        except:
            continue

    return quiz_list


# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.header("Controls")

    images = st.file_uploader(
        "Upload images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    pil_images = []

    if images:
        pil_images = [Image.open(img) for img in images]

        if len(pil_images) > 3:
            st.error("Max 3 images allowed")
            st.stop()

        st.subheader("Preview")
        cols = st.columns(len(pil_images))
        for i, img in enumerate(pil_images):
            with cols[i]:
                st.image(img)

    selected_language = st.selectbox(
            "Select a Language",
            ["Select language","English", "Bangla"]
            )

    selected_difficulty = st.selectbox(
            "Select Difficulty",
            ["Select difficulty","Easy", "Medium", "Hard"]
        )

    pressed = st.button("Generate AI Content", type="primary")


# ---------------- MAIN LOGIC ----------------
if pressed:

    if selected_language == "Select language":
        st.error("Please select a language")
        st.stop()

    if selected_difficulty == "Select difficulty":
        st.error("Please select difficulty")
        st.stop()

    if not pil_images:
        st.error("Upload at least 1 image")
        st.stop()

    # ---------------- NOTES ----------------
    with st.container(border=True):
        st.subheader("📝 Notes")

        with st.spinner("Generating notes..."):
            notes = note_generator(pil_images, selected_language)
            st.markdown(notes)

    # ---------------- AUDIO ----------------
    with st.container(border=True):
        st.subheader("🔊 Audio")

        clean_text = notes.replace("#", "").replace("*", "").replace("-", "")

        audio = audio_transcription(clean_text, selected_language)
        st.audio(audio, format="audio/mp3")

    # ---------------- QUIZ ----------------
    with st.container(border=True):
        st.subheader("🧠 Quiz")

        with st.spinner("Generating quiz..."):
            quiz_text = quiz_generator(pil_images, selected_difficulty, selected_language)
            st.session_state.quiz_data = parse_quiz(quiz_text)


# ---------------- QUIZ UI ----------------
if st.session_state.quiz_data:

    st.subheader("Interactive Quiz")

    for i, q in enumerate(st.session_state.quiz_data):

        st.write(q["question"])

        selected = st.radio(
            "Choose answer",
            q["options"],
            key=f"q{i}"
        )

        if st.button("Submit", key=f"s{i}"):

            correct_index = ord(q["answer"].upper()) - 65
            correct_answer = q["options"][correct_index]

            if selected == correct_answer:
                st.success("Correct ✅")
                st.session_state.score += 1
            else:
                st.error("Wrong ❌")
                st.info(f"Correct answer: {correct_answer}")

    st.write(f"🏆 Score: {st.session_state.score}")