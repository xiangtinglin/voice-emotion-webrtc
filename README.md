# WebRTC Whisper Emotion Chatbot

## 功能
- 使用 `streamlit-webrtc` 錄音（瀏覽器支援）
- 使用 `openai/whisper-tiny` 語音辨識
- 使用 HuggingFace 情緒分析模型
- 回應以 gTTS 語音合成播放

## 執行方式
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 部署方式
- 上傳整包到 GitHub
- Streamlit Cloud 指定主程式 `app.py`
