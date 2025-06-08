import streamlit as st
import tempfile
import os
from transformers import pipeline
from gtts import gTTS

st.title("🎤 Whisper 語音情緒聊天機器人 (無需 Azure)")

st.markdown("請錄音後送出語音，我們會將語音轉文字、分析情緒並以語音回覆你。")

# 錄音元件 (網頁錄音)
audio_bytes = st.file_uploader("上傳你的語音 (.wav/.mp3)", type=["wav", "mp3"])

if audio_bytes is not None:
    # 儲存成臨時檔
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
        tmp_audio.write(audio_bytes.read())
        tmp_path = tmp_audio.name

    # 語音辨識（Whisper）
    with st.spinner("語音辨識中..."):
        whisper = pipeline("automatic-speech-recognition", model="openai/whisper-small")
        result = whisper(tmp_path)
        text = result["text"]

    st.success(f"你說的是：{text}")

    # 情緒分析（情感分類）
    with st.spinner("情緒分析中..."):
        classifier = pipeline("sentiment-analysis")
        result = classifier(text)[0]
        label = result['label']
        score = result['score']
        st.write(f"情緒判定：{label}（信心值 {score:.2f}）")

    # 回應文字
    reply_text = f"你聽起來是 {label} 的情緒，我會記住你的感受。"

    # 文字轉語音 TTS
    tts = gTTS(reply_text, lang='zh')
    tts_path = os.path.join(tempfile.gettempdir(), "reply.mp3")
    tts.save(tts_path)

    # 播放語音
    with open(tts_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")

    st.markdown("🔁 可以重新錄音再試一次。")
