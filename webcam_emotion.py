import streamlit as st
from streamlit_webrtc import webrtc_streamer
from deepface import DeepFace
import av
import cv2

st.set_page_config(
    page_title="EmotionSense AI",
    page_icon="😊",
    layout="wide"
)

st.title("😊 EmotionSense AI")
st.subheader("Live Webcam Emotion Detection")


def video_frame_callback(frame):

    img = frame.to_ndarray(format="bgr24")

    try:

        result = DeepFace.analyze(
            img,
            actions=["emotion"],
            enforce_detection=False
        )

        emotions = result[0]["emotion"]
        dominant = result[0]["dominant_emotion"]

        confidence = emotions[dominant]

        sorted_emotions = sorted(
            emotions.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Main Emotion
        cv2.putText(
            img,
            f"{dominant.upper()} ({confidence:.1f}%)",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        # Top 3 Emotions
        y = 80

        for emo, score in sorted_emotions[:3]:

            cv2.putText(
                img,
                f"{emo.capitalize()}: {score:.1f}%",
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 0),
                2
            )

            y += 30

    except Exception as e:
        print(e)

    return av.VideoFrame.from_ndarray(
        img,
        format="bgr24"
    )


webrtc_streamer(
    key="emotion",
    video_frame_callback=video_frame_callback
)