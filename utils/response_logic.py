from transformers import pipeline

classifier = pipeline("sentiment-analysis")

def get_reply(text):
    result = classifier(text)[0]
    label = result["label"].lower()

    if "positive" in label:
        return result, "That's great to hear! How can I help further?"
    elif "negative" in label:
        return result, "I'm here for you. Do you want to talk more about it?"
    else:
        return result, "Thanks for sharing. Would you like to continue chatting?"
