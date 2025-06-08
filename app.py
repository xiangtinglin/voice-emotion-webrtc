import streamlit as st
from gtts import gTTS
import os
import random

st.set_page_config(page_title="Offline Emotion Voice Chatbot")
st.title("🎙️ Emotion Voice Chatbot (No Azure)")
st.markdown("輸入一句英文，我會模擬情緒分析並回覆你語音！")

text_input = st.text_input("請輸入一句英文句子：", "")

if st.button("Analyze & Respond"):
    if not text_input:
        st.warning("請先輸入一句英文句子")
        st.stop()

    # 模擬情緒分析
    sentiment = random.choice(["positive", "neutral", "negative"])
    st.write(f"🧠 模擬情緒分析結果：**{sentiment.upper()}**")

    # 根據情緒給出固定回應
    if sentiment == "positive":
        reply = "I'm happy to hear that!"
    elif sentiment == "negative":
        reply = "I'm sorry you're feeling this way."
    else:
        reply = "Thanks for sharing. I'm here for you."

    st.write(f"🤖 機器人回應：{reply}")

    # 文字轉語音（gTTS）
    tts = gTTS(reply)
    tts.save("static/response.mp3")
    st.audio("static/response.mp3")
