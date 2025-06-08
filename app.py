import streamlit as st
from streamlit_audio_recorder import audio_recorder
import tempfile
import torchaudio
from transformers import pipeline
from gtts import gTTS
import os

st.set_page_config(page_title="🎤 Voice Emotion Chatbot", layout="centered")
st.title("🎙️ Voice Emotion Chatbot Demo")

# 錄音區塊
st.markdown("## Step 1: 請錄音")
audio_bytes = audio_recorder(pause_threshold=3.0)

# 如果有錄到聲音
if audio_bytes:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes)
        audio_path = tmp.name

    st.success("✅ 錄音完成，開始辨識中...")

    # Whisper 語音辨識
    pipe = pipeline("automatic-speech-recognition", model="openai/whisper-small")
    result = pipe(audio_path)
    text = result["text"]
    st.markdown(f"**你說的是：** {text}")

    # 情緒分析
    classifier = pipeline("sentiment-analysis")
    sentiment = classifier(text)[0]
    st.markdown(f"**偵測到的情緒：** `{sentiment['label']}`（信心值：{sentiment['score']:.2f}）")

    # 回應語音
    response = f"你聽起來有點 {sentiment['label']}，一切還好嗎？"
    tts = gTTS(response, lang="zh")
    tts_path = os.path.join(tempfile.gettempdir(), "response.mp3")
    tts.save(tts_path)

    st.markdown("### 語音回應：")
    st.audio(tts_path)
