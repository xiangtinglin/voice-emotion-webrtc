import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import numpy as np
import av
import tempfile
import torch
import torchaudio
from transformers import pipeline, WhisperProcessor, WhisperForConditionalGeneration
from gtts import gTTS
import os
from io import BytesIO

st.set_page_config(page_title="WebRTC Emotion Voice Bot")

st.title("🎤 Whisper + Emotion + TTS 聲音聊天機器人")
st.markdown("👉 錄音、語音辨識、情緒分析、語音回應，全在網頁完成")

@st.cache_resource
def load_models():
    whisper_model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny", torch_dtype=torch.float32)
    whisper_processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
    sentiment_pipe = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
    return whisper_model, whisper_processor, sentiment_pipe

whisper_model, whisper_processor, sentiment_pipe = load_models()

class AudioProcessor(AudioProcessorBase):
    def __init__(self) -> None:
        self.recorded_frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        # 將音訊存下來
        pcm = frame.to_ndarray().flatten().astype(np.float32) / 32768.0  # 16-bit PCM to float32
        self.recorded_frames.append(pcm)
        return frame

    def get_audio(self):
        return np.concatenate(self.recorded_frames)

# 啟動錄音
ctx = webrtc_streamer(
    key="speech",
    mode="sendonly",
    in_audio=True,
    media_stream_constraints={"audio": True, "video": False},
    audio_processor_factory=AudioProcessor,
    async_processing=True,
)

if ctx.audio_processor:
    st.info("🎙️ 點選 Start 開始錄音，點 Stop 結束")

    if st.button("▶️ 分析錄音"):
        raw_audio = ctx.audio_processor.get_audio()
        ctx.audio_processor.recorded_frames = []

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            tensor = torch.tensor(raw_audio).unsqueeze(0)
            torchaudio.save(tmpfile.name, tensor, 16000)
            st.audio(tmpfile.name)

            # Whisper
            waveform, _ = torchaudio.load(tmpfile.name)
            input_features = whisper_processor(waveform.squeeze(), sampling_rate=16000, return_tensors="pt").input_features
            predicted_ids = whisper_model.generate(input_features)
            transcription = whisper_processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
            st.success(f"你說的是：「{transcription}」")

            # Sentiment
            sentiment = sentiment_pipe(transcription)[0]["label"].lower()
            st.write(f"🧠 情緒分析：**{sentiment.upper()}**")

            # Response
            if sentiment == "positive":
                reply = "I'm happy to hear that!"
            elif sentiment == "negative":
                reply = "I'm sorry you're feeling this way."
            else:
                reply = "Thanks for sharing."

            st.write(f"🤖 回應：{reply}")
            tts = gTTS(reply)
            tts_path = os.path.join("static", "response.mp3")
            tts.save(tts_path)
            st.audio(tts_path)
