import streamlit as st
from gtts import gTTS
import os
from utils.response_logic import get_reply

st.set_page_config(page_title="Real Emotion Chatbot")
st.title("🎙️ Real Emotion Chatbot (English)")
st.markdown("輸入英文句子，我會分析情緒並用語音回覆你！")

user_input = st.text_input("請輸入一句英文句子：", "")

if st.button("Analyze & Respond"):
    if not user_input:
        st.warning("請先輸入英文句子")
        st.stop()

    result, reply = get_reply(user_input)
    st.write(f"🧠 **情緒分析：{result['label']} ({round(result['score'] * 100, 2)}%)**")
    st.write(f"🤖 機器人回應：{reply}")

    # TTS 產生語音
    tts = gTTS(reply)
    mp3_path = "static/response.mp3"
    tts.save(mp3_path)
    st.audio(mp3_path)
