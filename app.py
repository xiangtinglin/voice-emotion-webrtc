import streamlit as st
import speech_recognition as sr
from transformers import pipeline
from gtts import gTTS
import os

st.set_page_config(page_title="Voice Emotion Chatbot", layout="centered")
st.title("🎤 Voice Emotion Chatbot (No Azure)")
st.markdown("用英文說話，我會辨識你的情緒並用語音回應你！")

# 初始化情緒分析器
@st.cache_resource
def load_sentiment_pipeline():
    return pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

sentiment_analyzer = load_sentiment_pipeline()

# 錄音辨識功能
def recognize_from_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("請開始說話（錄音中）...")
        audio = recognizer.listen(source, phrase_time_limit=5)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            st.error("辨識失敗，請再說一次")
        except sr.RequestError as e:
            st.error(f"語音服務錯誤: {e}")
    return None

# 回應生成邏輯
def generate_response(sentiment_label):
    if sentiment_label == "positive":
        return "I'm really glad to hear that!"
    elif sentiment_label == "negative":
        return "I'm sorry you're feeling this way. I'm here if you want to talk."
    else:
        return "Thanks for sharing. I'm listening."

# 主流程按鈕
if st.button("🎙️ Start Talking"):
    text = recognize_from_microphone()
    if text:
        st.success(f"你說的是："{text}"")
        result = sentiment_analyzer(text)[0]
        label = result["label"].lower()
        st.write(f"🧠 偵測到的情緒：**{label.upper()}**")

        reply = generate_response(label)
        st.write(f"🤖 機器人回應：{reply}")

        # 文字轉語音
        tts = gTTS(reply)
        tts.save("static/response.mp3")
        st.audio("static/response.mp3")
