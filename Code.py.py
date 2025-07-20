import streamlit as st
from PIL import Image
import io
import requests
from transformers import pipeline
from gtts import gTTS
import tempfile
from diffusers import StableDiffusionPipeline
import torch

# --- Page Config ---
st.set_page_config(page_title="Creative StoryTelling with AI", page_icon="🖼️")

# --- Custom Styling ---
st.markdown("""
    <style>
    .stApp {
        background-color: #bfbfbf;
        color: #1a1a1a;
    }
    .block-container {
        padding-top: 3.5rem;
        padding-bottom: 2rem;
    }
    .custom-warning {
        background-color: #fff0f0;
        padding: 12px;
        border-left: 5px solid #ff4d4d;
        border-radius: 5px;
        color: #cc0000;
        font-weight: bold;
        margin-top: 1rem;
    }
    .upload-label {
        font-size: 22px;
        font-weight: bold;
        color: #198c00;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    div[data-testid="stButton"] > button {
        background: linear-gradient(to right, #4B0082, #8A2BE2);
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 16px;
        border: none;
        transition: background 0.3s ease;
    }
    div[data-testid="stButton"] > button:hover {
        background: linear-gradient(to right, #6A0DAD, #9F2BFF);
    }
    .header-title {
        text-align: center;
        color: #6700d4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .header-sub {
        text-align: center;
        font-size: 1.5rem;
        color: #4B0082;
        margin-bottom: 1.5rem;
        font-family: sans-serif;
        font-weight: bold;
    }
    .stImage {
        border: 1px solid #ccc;
        border-radius: 8px;
        color: black;
    }
    .caption-text {
        font-size: 16px;
        color: #333;
        margin-bottom: 1rem;
    }
    .story-text {
        font-size: 18px;
        color: #1a1a1a;
        line-height: 1.6;
    }
    section[data-testid="stSidebar"] {
        background-color: #d9d9d9;
    }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("Algorithm")
page = st.sidebar.radio("", ["📷 Image to Story", "📝 Story to Image"])

# --- Header ---
st.markdown('<div class="header-sub">Balaj P S (20MIY0057)</div>', unsafe_allow_html=True)
st.markdown('<div class="header-title">🎨Creative StoryTelling<br>with <br>Artificial Intelligence🤖</div>', unsafe_allow_html=True)

# --- Load Pipelines ---
@st.cache_resource
def load_image_to_text_pipeline():
    return pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

@st.cache_resource
def load_text_to_image_pipeline():
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float32
    ).to("cpu")
    return pipe

# --- Functions ---
def image_2_text(image_file, image_to_text_pipeline):
    try:
        image = Image.open(io.BytesIO(image_file.read()))
        text = image_to_text_pipeline(image)
        if isinstance(text, list) and len(text) > 0 and isinstance(text[0], dict):
            return text[0].get('generated_text', 'No caption found')
        return "No caption found"
    except Exception as e:
        return f"An error occurred: {e}"

def generate_story_from_captions(captions):
    try:
        url = 'https://magicloops.dev/api/loop/API KEY' #Replace with the API KEY
        response = requests.post(url, json=captions)
        if response.status_code == 200:
            response_json = response.json()
            return response_json.get("story", "No 'story' key in response.")
        else:
            return f"Failed to generate story. Status Code: {response.status_code}"
    except Exception as e:
        return f"An error occurred while calling Magic Loops API: {e}"

def text_to_speech(message):
    try:
        tts = gTTS(text=message, lang='en', tld='co.in')
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        return temp_file.name
    except Exception as e:
        return None

# --- Load Pipelines Once ---
image_to_text_pipeline = load_image_to_text_pipeline()
text_to_image_pipeline = load_text_to_image_pipeline()

# --- Page 1: Image to Story ---
if page == "📷 Image to Story":
    st.markdown('<div class="upload-label">📄 Upload Images in Order</div>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader("", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

    if "captions" not in st.session_state:
        st.session_state.captions = []
    if "story" not in st.session_state:
        st.session_state.story = None

    if uploaded_files:
        st.session_state.captions.clear()

        for i, uploaded_file in enumerate(uploaded_files):
            st.image(uploaded_file, caption=f"🖼️ Image {i+1}")
            with st.spinner(f"Generating caption for Image {i+1}..."):
                caption = image_2_text(uploaded_file, image_to_text_pipeline)
                st.session_state.captions.append(caption)
                st.markdown(f"<div class='caption-text'><strong>Caption {i+1}:</strong> {caption}</div>", unsafe_allow_html=True)

    if st.session_state.captions:
        if st.button("✨ Generate Story"):
            with st.spinner("Generating story from captions..."):
                story_text = generate_story_from_captions(st.session_state.captions)
                st.session_state.story = story_text

                st.subheader("📖 Generated Story")
                st.markdown(f"<div class='story-text'>{story_text}</div>", unsafe_allow_html=True)

            with st.spinner("Generating audio..."):
                audio_file_path = text_to_speech(st.session_state.story)
                if audio_file_path:
                    st.audio(audio_file_path, format="audio/mp3")
                else:
                    st.error("❌ Failed to generate audio.")
    else:
        st.markdown("""
            <div class="custom-warning">
                ⚠️ Please upload images to generate captions.
            </div>
        """, unsafe_allow_html=True)

# --- Page 2: Story to Image ---
elif page == "📝 Story to Image":
    st.markdown('<div class="upload-label">📝 Enter Story Prompt Below</div>', unsafe_allow_html=True)

    story_input = st.text_area("Enter your story or text prompt:", height=200)

    if st.button("🎨 Generate Image"):
        if story_input.strip():
            with st.spinner("Generating image from story..."):
                result = text_to_image_pipeline(story_input)
                image = result.images[0]
                st.image(image, caption="🎨 Generated Image", use_container_width=True)

                img_bytes = io.BytesIO()
                image.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                st.download_button(
                    label="📅 Download Image",
                    data=img_bytes,
                    file_name="generated_image.png",
                    mime="image/png"
                )
        else:
            st.warning("⚠️ Please enter a story or text prompt.")
