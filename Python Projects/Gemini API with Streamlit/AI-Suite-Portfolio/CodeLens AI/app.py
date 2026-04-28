import streamlit as st
from PIL import Image
from api_calling import analyze_image

st.title("🧠 CodeLens AI")
st.markdown("Upload code/error image and get Debug, Hint or Solution")

# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload Image",
    type=["png", "jpg", "jpeg"]
)

image = None

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# ---------------- MODE ----------------
mode = st.selectbox(
    "Choose Mode",
    ["Select", "Debug", "Hint", "Solution"]
)

# ---------------- ACTION ----------------
if st.button("Analyze"):

    if not image:
        st.error("Upload an image first")
        st.stop()

    if mode == "Select":
        st.error("Select Debug / Hint / Solution")
        st.stop()

    with st.spinner("AI is thinking..."):

        result = analyze_image(image, mode)

        st.subheader("Result")
        st.markdown(result)