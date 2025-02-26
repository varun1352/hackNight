import streamlit as st
import requests
from PIL import Image
import io

# Replace these with your actual Lightning endpoints
QWEN_URL = "https://8000-dep-01jmzyskh4xrsacxs58nkhfxca-d.cloudspaces.litng.ai/predict"
JANUS_URL = "https://8000-dep-01jmzyerzfqt3yeb1sz3wnd5c1-d.cloudspaces.litng.ai/predict"

def call_endpoint(url, image_bytes, question):
    """
    Sends a POST request to the /predict endpoint.
    Adjust the data/headers as needed for your model's expected format.
    """
    # Example: multipart form-data with "file" and a "question" field
    files = {
        "file": ("uploaded_image.jpg", image_bytes, "image/jpeg")
    }
    data = {
        "question": question
    }
    try:
        response = requests.post(url, files=files, data=data, timeout=120)
        response.raise_for_status()  # Raise HTTPError if status != 200
        # If your endpoint returns JSON, parse it:
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Error calling endpoint: {e}"

st.title("Compare 2 VLMs via Lightning AI")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
question = st.text_input("Enter a question or prompt about the image:")

if st.button("Run Models"):
    if not uploaded_file:
        st.warning("Please upload an image first.")
    else:
        image_bytes = uploaded_file.read()
        st.image(Image.open(io.BytesIO(image_bytes)), caption="Uploaded Image")

        with st.spinner("Calling Qwen endpoint..."):
            qwen_result = call_endpoint(QWEN_URL, image_bytes, question)

        with st.spinner("Calling Janus endpoint..."):
            janus_result = call_endpoint(JANUS_URL, image_bytes, question)

        # Display side by side
        col1, col2 = st.columns(2)
        col1.subheader("Qwen Output")
        col1.write(qwen_result)

        col2.subheader("Janus Output")
        col2.write(janus_result)
