import streamlit as st
import streamlit.components.v1 as components
import tempfile
import base64
import os
from transformers import pipeline
from gtts import gTTS

st.set_page_config(page_title="🎤 Whisper Voice Chat", layout="centered")
st.title("🗣️ Whisper 語音情緒聊天機器人")

# 錄音 HTML 元件
st.markdown("### Step 1: 錄音")
components.html("""
    <script>
    let mediaRecorder;
    let audioChunks = [];
    let startBtn, stopBtn;

    function createRecorderUI() {
        const container = document.createElement("div");

        startBtn = document.createElement("button");
        startBtn.innerText = "🎙️ 開始錄音";
        startBtn.onclick = startRecording;

        stopBtn = document.createElement("button");
        stopBtn.innerText = "🛑 停止錄音";
        stopBtn.onclick = stopRecording;
        stopBtn.disabled = true;

        container.appendChild(startBtn);
        container.appendChild(stopBtn);
        document.body.appendChild(container);
    }

    async function startRecording() {
        audioChunks = [];
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
        mediaRecorder.onstop = () => {
            const blob = new Blob(audioChunks, { type: 'audio/wav' });
            const reader = new FileReader();
            reader.onloadend = () => {
                const base64Audio = reader.result.split(',')[1];
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = '/';
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'audio';
                input.value = base64Audio;
                form.appendChild(input);
                document.body.appendChild(form);
                form.submit();
            };
            reader.readAsDataURL(blob);
        };
        startBtn.disabled = true;
        stopBtn.disabled = false;
    }

    function stopRecording() {
        mediaRecorder.stop();
        startBtn.disabled = false;
        stopBtn.disabled = true;
    }

    createRecorderUI();
    </script>
""", height=150)

# 接收音訊
if "audio" in st.experimental_get_query_params():
    audio_b64 = st.experimental_get_query_params()["audio"][0]
    audio_bytes = base64.b64decode(audio_b64)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_bytes)
        audio_path = f.name

    st.success("✅ 錄音接收成功，開始語音辨識中...")

    # Whisper 模型
    asr = pipeline("automatic-speech-recognition", model="openai/whisper-small")
    result = asr(audio_path)
    text = result["text"]

    st.markdown(f"**你說的是：** {text}")

    # 情緒分析
    clf = pipeline("sentiment-analysis")
    sentiment = clf(text)[0]
    st.markdown(f"**偵測到情緒：** `{sentiment['label']}`（信心值：{sentiment['score']:.2f}）")

    # 回應語音
    response = f"你聽起來有些 {sentiment['label']}，要不要聊聊呢？"
    tts = gTTS(response, lang='zh')
    tts_path = os.path.join(tempfile.gettempdir(), "response.mp3")
    tts.save(tts_path)

    st.audio(tts_path)
