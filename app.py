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


# import streamlit as st
# from PIL import Image
# import io

# # Lightning AIHub for calling deployed endpoints
# from lightning_sdk import AIHub

# # DSPy for pipeline steps
# from dspy import Pipeline, step

# ##############################
# # 1) SETUP ENDPOINTS
# ##############################
# def load_deployments():
#     """Initialize references to the two VLM endpoints."""
#     hub = AIHub()

#     # Qwen 2.5 VL
#     deployment_qwen = hub.run(
#         "temp_01jjt2pkg54t138gsx6ryk0gmr",
#         teamspace="vision-model",
#         user="vd2298"
#     )

#     # DeepSeek Janus Pro
#     deployment_janus = hub.run(
#         "temp_01jmwv37z2nvmf2d6kk7yhsn26",
#         teamspace="vision-model",
#         user="vd2298"
#     )
#     return deployment_qwen, deployment_janus

# deployment_qwen, deployment_janus = load_deployments()

# ##############################
# # 2) DEFINE DSPy STEPS
# ##############################

# @step
# def run_qwen(context):
#     """Call Qwen endpoint with the user's image+question."""
#     deployment = context["deployment_qwen"]
#     payload = context["inputs"]
#     context["qwen_result"] = deployment.run(payload)
#     return context

# @step
# def run_janus(context):
#     """Call Janus endpoint with the user's image+question."""
#     deployment = context["deployment_janus"]
#     payload = context["inputs"]
#     context["janus_result"] = deployment.run(payload)
#     return context

# @step
# def compare_outputs(context):
#     """Simple check if Qwen and Janus outputs are identical strings."""
#     qwen_res = context["qwen_result"]
#     janus_res = context["janus_result"]

#     # Depending on your endpoints, these might be dicts, strings, or JSON.
#     # Adjust comparison logic as needed. Here, assume they're strings.
#     same_text = (str(qwen_res).strip() == str(janus_res).strip())
#     context["are_same"] = same_text

#     return context

# # 3) Build a pipeline with these steps, in order:
# pipeline = Pipeline(steps=[
#     run_qwen,
#     run_janus,
#     compare_outputs
# ])

# ##############################
# # 4) STREAMLIT UI
# ##############################
# st.title("Compare 2 VLMs (Qwen 2.5 VL + Janus)")

# uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
# question = st.text_input("Enter a question or prompt about the image:")

# if st.button("Run Models"):
#     if not uploaded_file:
#         st.warning("Please upload an image first.")
#     else:
#         # Read file into bytes
#         image_bytes = uploaded_file.read()
#         # Display the uploaded image
#         st.image(Image.open(io.BytesIO(image_bytes)), caption="Uploaded Image")

#         # Prepare the input payload for each endpoint
#         # Adjust keys to match how your endpoints expect data
#         input_payload = {
#             "image": image_bytes,
#             "question": question
#         }

#         # Create pipeline context
#         context = {
#             "deployment_qwen": deployment_qwen,
#             "deployment_janus": deployment_janus,
#             "inputs": input_payload
#         }

#         with st.spinner("Running Qwen inference..."):
#             # The pipeline step run_qwen is called
#             # but pipeline is a chain; it will call each step in order
#             # We'll call the entire pipeline once to get all results
#             result_context = pipeline(context)

#         # Retrieve pipeline outputs
#         result_qwen = result_context["qwen_result"]
#         result_janus = result_context["janus_result"]
#         are_same = result_context["are_same"]

#         # Display side-by-side
#         col1, col2 = st.columns(2)
#         col1.subheader("Qwen 2.5 VL Output")
#         col1.write(result_qwen)

#         col2.subheader("DeepSeek Janus Pro Output")
#         col2.write(result_janus)

#         # Indicate whether they matched
#         st.write("---")
#         if are_same:
#             st.success("Both VLMs produced the **same** output!")
#         else:
#             st.info("The two VLM outputs **differ**.")
