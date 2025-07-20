# Creative-Storytelling-with-AI
A Streamlit web app that transforms images into narrated stories and generates visuals from written prompts using powerful AI models like BLIP, Stable Diffusion, and gTTS.

# 🎨 Creative Storytelling Using Artificial Intelligence 🤖

A Streamlit-based web app that transforms uploaded images into narrated stories and generates artwork from written prompts. Powered by AI models like BLIP, Stable Diffusion, and gTTS.

---

## 🌟 Features

### 📷 Image to Story
- Upload a sequence of images.
- Captions are generated using **BLIP (Salesforce)**.
- A full story is created from these captions using the **Magic Loops API**.
- The story is narrated using **Google Text-to-Speech (gTTS)**.

### 📝 Story to Image
- Enter a text prompt or story.
- Generate beautiful visuals using **Stable Diffusion**.

### 🎧 Audio Narration
- Enjoy listening to the AI-generated stories in MP3 format.

### 🖼️ Clean & Responsive UI
- Streamlit with custom CSS styling for a better user experience.

---

## 🛠️ Technologies Used

- [Streamlit](https://streamlit.io/) – Web app framework
- [Transformers (Hugging Face)](https://huggingface.co/docs/transformers) – Image captioning
- [Diffusers (Hugging Face)](https://huggingface.co/docs/diffusers) – Text-to-image generation
- [gTTS](https://pypi.org/project/gTTS/) – Text-to-speech
- [Magic Loops API](https://magicloops.dev/) – Story generation
- [Pillow (PIL)](https://pillow.readthedocs.io/) – Image processing
- [Torch](https://pytorch.org/) – Backend for AI models

---

## 🔐 API Key Setup – Magic Loops

To generate stories from captions, you'll need a **Magic Loops API key**.

### Steps:

1. Sign up at [https://magicloops.dev](https://magicloops.dev).
2. Create a new **Loop** that takes a list of captions and returns a story.
3. Copy your **Loop API endpoint**.
4. In `app2.py`, replace the default URL:
   ```python
   url = 'https://magicloops.dev/api/loop/YOUR-LOOP-ID/run'

## 🚀 Getting Started

### 1. Clone the Repository

git clone https://github.com/Balajps12/Creative-Storytelling-with-AI.git

cd Creative-Storytelling-with-AI

pip install -r requirements.txt

streamlit run Code.py
