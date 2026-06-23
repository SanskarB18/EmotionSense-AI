import streamlit as st
from deepface import DeepFace
from PIL import Image
import tempfile
from streamlit_webrtc import webrtc_streamer
from deepface import DeepFace
import av
import cv2
from utils.recommender import get_recommendations

import streamlit as st

import os
import pandas as pd
from datetime import datetime

os.makedirs("snapshots", exist_ok=True)
os.makedirs("history", exist_ok=True)

csv_path = "history/emotion_history.csv"
if not os.path.exists(csv_path):

    columns = [
        "Timestamp",
        "DominantEmotion",
        "Happy",
        "Neutral",
        "Sad",
        "Angry",
        "Fear",
        "Surprise",
        "Disgust",
        "UserNote",
        "ImagePath"
    ]

    pd.DataFrame(columns=columns).to_csv(
        csv_path,
        index=False
    )




st.set_page_config(
    page_title="EmotionSense AI",
    page_icon="",
    layout="wide"
)
# =====================================
# GLOBAL STYLING
# =====================================

st.markdown("""
<style>

/* Sidebar */

section[data-testid="stSidebar"]{
    background-color:#0f172a;
    border-right:1px solid rgba(255,255,255,0.08);
}

/* Sidebar text */

section[data-testid="stSidebar"] *{
    color:white;
}

/* Navigation spacing */

div[role="radiogroup"]{
    gap:12px;
}

/* Navigation item text */

div[role="radiogroup"] label{
    font-size:17px !important;
    font-weight:500 !important;
}

/* Main app */

.main{
    background-color:#020617;
}

/* Headers */

h1,h2,h3{
    color:#f8fafc;
}

/* Paragraphs */

p{
    color:#cbd5e1;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# SIDEBAR HEADER
# =====================================

st.sidebar.markdown("""
<div style="
text-align:center;
padding-top:15px;
padding-bottom:25px;
">

<div style="
font-size:56px;
margin-bottom:8px;
">
🧠
</div>

<h2 style="
font-size:28px;
margin-bottom:5px;
">
EmotionSense AI
</h2>

<p style="
color:#94a3b8;
font-size:14px;
margin-top:0;
">
Emotion Intelligence Platform
</p>

</div>
""", unsafe_allow_html=True)

# =====================================
# NAVIGATION
# =====================================

if "page" not in st.session_state:

    st.session_state.page = "🏠 Home"

pages = [
    "🏠 Home",
    "📷 Upload Image",
    "🎥 Live Webcam",
    "📸 Snapshot Mode",
    "📜 History",
    "📅 Reports",
    "🎯 Trained ResNet50 Model",
    "📄 PDF Report"
]

page = st.sidebar.radio(
    "",
    pages,
    index=pages.index(
        st.session_state.page
    ),
    label_visibility="collapsed"
)

st.session_state.page = page

st.session_state.page = page


if page == "📷 Upload Image":

    st.title("📷 Upload Image")

    uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["jpg", "jpeg", "png"]
)

    # ----------------------------------
    # Emotion Detection
    # ----------------------------------

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            image.save(tmp.name)

            result = DeepFace.analyze(
                img_path=tmp.name,
                actions=["emotion"],
                enforce_detection=False
            )

        emotion = result[0]["dominant_emotion"]
        emotion_scores = result[0]["emotion"]

        confidence = emotion_scores[emotion]

        songs, movies, quote, actions, productivity = (
            get_recommendations(emotion)
        )

        # Recommendations

        songs, movies, quote, actions, productivity = (
            get_recommendations(emotion)
        )

        # ----------------------------------
        # Layout
        # ----------------------------------

        col1, col2 = st.columns([1, 1])

        with col1:

            st.image(
                image,
                caption="Uploaded Image",
                use_container_width=True
            )

        with col2:

            st.metric(
                "Detected Emotion",
                emotion.upper()
            )

            st.subheader("Top 3 Emotions")

            sorted_emotions = sorted(
                emotion_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )

            for emo, score in sorted_emotions[:3]:

                st.write(
                    f"**{emo.capitalize()}** — {score:.2f}%"
                )

                st.progress(float(score) / 100)



        st.divider()

        st.header("📓 Mood Journal")

        user_note = st.text_area(
            "Why do you think you're feeling this way today?",
            height=120,
            placeholder="Example: Had a great day with friends..."
        )

        # ----------------------------------
        # Recommendations
        st.divider()
        st.header("🎯 Recommendation Center")

        # ==================================
        # SONGS + MOVIES
        # ==================================

        col1, col2 = st.columns(2)

        songs_html = "".join([
        f"""
        <div style="
        padding:12px;
        margin-bottom:10px;
        border-radius:12px;
        background:rgba(255,255,255,0.04);
        ">
        🎵 {song}
        </div>
        """
        for song in songs
        ])

        movies_html = "".join([
        f"""
        <div style="
        padding:12px;
        margin-bottom:10px;
        border-radius:12px;
        background:rgba(255,255,255,0.04);
        ">
        🎬 {movie}
        </div>
        """
        for movie in movies
        ])

        col1, col2 = st.columns(2)

        with col1:

            with st.container(border=True):

                st.subheader("🎵 Recommended Songs")

                for song in songs:

                    st.markdown(f"""
                    <div style="
                    padding:12px;
                    margin-bottom:10px;
                    border-radius:12px;
                    background:rgba(255,255,255,0.04);
                    ">
                    🎵 {song}
                    </div>
                    """, unsafe_allow_html=True)

        with col2:

            with st.container(border=True):

                st.subheader("🎬 Recommended Movies")

                for movie in movies:

                    st.markdown(f"""
                    <div style="
                    padding:12px;
                    margin-bottom:10px;
                    border-radius:12px;
                    background:rgba(255,255,255,0.04);
                    ">
                    🎬 {movie}
                    </div>
                    """, unsafe_allow_html=True)

        # ==================================
        # QUOTE
    

        st.write("")

        with st.container(border=True):

            st.subheader("💡 Quote of the Moment")

            st.markdown(f"""
            <div style="
            font-size:22px;
            padding:10px;
            color:#e2e8f0;
            ">
            {quote}
            </div>
            """, unsafe_allow_html=True)


       # ==================================
        # ACTIONS + PRODUCTIVITY
        # ==================================

        st.write("")

        col1, col2 = st.columns(2)

        # ----------------------------------
        # ACTION RECOMMENDATIONS
        # ----------------------------------

        with col1:

            with st.container(border=True):

                st.subheader("📌 Action Recommendation")

                st.markdown("""
                <div style="
                padding:14px;
                margin-bottom:18px;
                border-radius:12px;
                background:rgba(34,197,94,0.15);
                font-size:18px;
                ">
                💡 Actions create lasting emotional improvement.
                </div>
                """, unsafe_allow_html=True)

                for action in actions:

                    st.markdown(f"""
                    <div style="
                    padding:16px;
                    margin-bottom:12px;
                    border-radius:12px;
                    background:rgba(255,255,255,0.04);
                    font-size:18px;
                    ">
                    🎯 {action}
                    </div>
                    """, unsafe_allow_html=True)

        # ----------------------------------
        # PRODUCTIVITY COACH
        # ----------------------------------

        with col2:

            with st.container(border=True):

                st.subheader("🧠 Productivity Coach")

                st.markdown(f"""
                <div style="
                padding:14px;
                margin-bottom:18px;
                border-radius:12px;
                background:rgba(34,197,94,0.15);
                font-size:18px;
                ">
                💡 {productivity["advice"]}
                </div>
                """, unsafe_allow_html=True)

                for task in productivity["tasks"]:

                    st.markdown(f"""
                    <div style="
                    padding:16px;
                    margin-bottom:12px;
                    border-radius:12px;
                    background:rgba(255,255,255,0.04);
                    font-size:18px;
                    ">
                    🚀 {task}
                    </div>
                    """, unsafe_allow_html=True)

                # ----------------------------------

        st.divider()

        if st.button(
            "💾 Save Entry",
            use_container_width=True
        ):

            if not user_note.strip():

                st.warning(
                    "⚠ Please complete your mood journal first."
                )

            else:

                timestamp_file = datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )

                image_path = (
                    f"snapshots/{timestamp_file}.jpg"
                )

                image.save(image_path)

                record = {
                    "Timestamp": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                    "DominantEmotion": emotion.capitalize(),

                    "Happy": emotion_scores.get(
                        "happy", 0
                    ),

                    "Neutral": emotion_scores.get(
                        "neutral", 0
                    ),

                    "Sad": emotion_scores.get(
                        "sad", 0
                    ),

                    "Angry": emotion_scores.get(
                        "angry", 0
                    ),

                    "Fear": emotion_scores.get(
                        "fear", 0
                    ),

                    "Surprise": emotion_scores.get(
                        "surprise", 0
                    ),

                    "Disgust": emotion_scores.get(
                        "disgust", 0
                    ),

                    "UserNote": user_note,

                    "ImagePath": image_path
                }

                pd.DataFrame([record]).to_csv(
                    csv_path,
                    mode="a",
                    header=not os.path.exists(csv_path)
                        or os.path.getsize(csv_path) == 0,
                    index=False
                )

                st.success(
                    "✅ Entry Saved Successfully"
                )

        # Footer
        # ----------------------------------

        st.divider()

        st.caption(
            "EmotionSense AI • DeepFace + Streamlit + Recommendation Engine"
        )


elif page == "🎥 Live Webcam":

    st.title("🎥 Live Webcam")

    st.write(
        "Live Emotion Detection using DeepFace"
    )

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

            cv2.putText(
                img,
                f"{dominant.upper()} ({confidence:.1f}%)",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

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

        except Exception:
            pass

        return av.VideoFrame.from_ndarray(
            img,
            format="bgr24"
        )

    webrtc_streamer(
        key="emotion",
        video_frame_callback=video_frame_callback
    )


elif page == "📸 Snapshot Mode":

    import pandas as pd
    import os
    from datetime import datetime

    st.title("📸 Snapshot Mode")

    st.write(
        "Capture your emotion, review the report, then save it."
    )


    if "analyzed" not in st.session_state:
        st.session_state.analyzed = False

    if "emotion_data" not in st.session_state:
        st.session_state.emotion_data = None

    if "captured_image" not in st.session_state:
        st.session_state.captured_image = None

    picture = st.camera_input("Take a Picture")

    if picture and not st.session_state.analyzed:

        image = Image.open(picture)

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jpg"
        ) as tmp:

            image.save(tmp.name)

            result = DeepFace.analyze(
                img_path=tmp.name,
                actions=["emotion"],
                enforce_detection=False
            )

        st.session_state.analyzed = True
        st.session_state.captured_image = image
        st.session_state.emotion_data = result

    if st.session_state.analyzed:

        image = st.session_state.captured_image
        result = st.session_state.emotion_data

        emotions = result[0]["emotion"]
        dominant = result[0]["dominant_emotion"]
        songs, movies, quote, actions, productivity = (
            get_recommendations(dominant)
        )

        # ==================================
        # SNAPSHOT RESULT
        # ==================================

        col1, col2 = st.columns([1, 1])

        with col1:

            st.image(
                image,
                caption="Captured Snapshot",
                use_container_width=True
            )

        with col2:

            st.subheader("🧠 Emotion Analysis")

            confidence = emotions[dominant]

            st.metric(
                "Detected Emotion",
                dominant.upper()
            )

            st.success(
                f"Primary Emotion: {dominant.capitalize()}"
            )

        # ==================================
        # TOP 3 EMOTIONS
        # ==================================

        st.divider()

        st.subheader("📊 Top 3 Emotions")

        sorted_emotions = sorted(
            emotions.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for emo, score in sorted_emotions[:3]:

            st.write(
                f"**{emo.capitalize()}** — {score:.2f}%"
            )

            st.progress(
                float(score) / 100
            )

        # ==================================
        # MOOD JOURNAL
        # ==================================

        st.divider()

        st.header("📓 Mood Journal")

        user_note = st.text_area(
            "Why do you think you're feeling this way today?",
            height=120,
            placeholder="Example: Had a great day with friends..."
        )

        journal_complete = bool(
            user_note.strip()
        )

        if not journal_complete:

            st.info(
                "📝 Please write a short journal note before saving."
            )

        # Recommendations
        st.divider()
        st.header("🎯 Recommendation Center")

        # ==================================
        # SONGS + MOVIES
        # ==================================

        col1, col2 = st.columns(2)

        songs_html = "".join([
        f"""
        <div style="
        padding:12px;
        margin-bottom:10px;
        border-radius:12px;
        background:rgba(255,255,255,0.04);
        ">
        🎵 {song}
        </div>
        """
        for song in songs
        ])

        movies_html = "".join([
        f"""
        <div style="
        padding:12px;
        margin-bottom:10px;
        border-radius:12px;
        background:rgba(255,255,255,0.04);
        ">
        🎬 {movie}
        </div>
        """
        for movie in movies
        ])

        col1, col2 = st.columns(2)

        with col1:

            with st.container(border=True):

                st.subheader("🎵 Recommended Songs")

                for song in songs:

                    st.markdown(f"""
                    <div style="
                    padding:12px;
                    margin-bottom:10px;
                    border-radius:12px;
                    background:rgba(255,255,255,0.04);
                    ">
                    🎵 {song}
                    </div>
                    """, unsafe_allow_html=True)

        with col2:

            with st.container(border=True):

                st.subheader("🎬 Recommended Movies")

                for movie in movies:

                    st.markdown(f"""
                    <div style="
                    padding:12px;
                    margin-bottom:10px;
                    border-radius:12px;
                    background:rgba(255,255,255,0.04);
                    ">
                    🎬 {movie}
                    </div>
                    """, unsafe_allow_html=True)

        # ==================================
        # QUOTE
    

        st.write("")

        with st.container(border=True):

            st.subheader("💡 Quote of the Moment")

            st.markdown(f"""
            <div style="
            font-size:22px;
            padding:10px;
            color:#e2e8f0;
            ">
            {quote}
            </div>
            """, unsafe_allow_html=True)


       # ==================================
        # ACTIONS + PRODUCTIVITY
        # ==================================

        st.write("")

        col1, col2 = st.columns(2)

        # ----------------------------------
        # ACTION RECOMMENDATIONS
        # ----------------------------------

        with col1:

            with st.container(border=True):

                st.subheader("📌 Action Recommendation")

                st.markdown("""
                <div style="
                padding:14px;
                margin-bottom:18px;
                border-radius:12px;
                background:rgba(34,197,94,0.15);
                font-size:18px;
                ">
                💡 Actions create lasting emotional improvement.
                </div>
                """, unsafe_allow_html=True)

                for action in actions:

                    st.markdown(f"""
                    <div style="
                    padding:16px;
                    margin-bottom:12px;
                    border-radius:12px;
                    background:rgba(255,255,255,0.04);
                    font-size:18px;
                    ">
                    🎯 {action}
                    </div>
                    """, unsafe_allow_html=True)

        # ----------------------------------
        # PRODUCTIVITY COACH
        # ----------------------------------

        with col2:

            with st.container(border=True):

                st.subheader("🧠 Productivity Coach")

                st.markdown(f"""
                <div style="
                padding:14px;
                margin-bottom:18px;
                border-radius:12px;
                background:rgba(34,197,94,0.15);
                font-size:18px;
                ">
                💡 {productivity["advice"]}
                </div>
                """, unsafe_allow_html=True)

                for task in productivity["tasks"]:

                    st.markdown(f"""
                    <div style="
                    padding:16px;
                    margin-bottom:12px;
                    border-radius:12px;
                    background:rgba(255,255,255,0.04);
                    font-size:18px;
                    ">
                    🚀 {task}
                    </div>
                    """, unsafe_allow_html=True)

        

        # ==================================
        # SAVE + RESET BUTTONS
        # ==================================

        st.divider()

        col1, col2 = st.columns(2)

        # ------------------
        # SAVE BUTTON
        # ------------------

        with col1:

            if st.button(
                "💾 Save Entry",
                use_container_width=True
            ):

                if not user_note.strip():

                    st.warning(
                        "⚠ Please write a journal note before saving."
                    )

                else:

                    timestamp_file = datetime.now().strftime(
                        "%Y%m%d_%H%M%S"
                    )

                    image_path = (
                        f"snapshots/{timestamp_file}.jpg"
                    )

                    image.save(image_path)

                    record = {

                        "Timestamp": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),

                        "DominantEmotion": dominant.capitalize(),

                        "Happy": emotions.get(
                            "happy", 0
                        ),

                        "Neutral": emotions.get(
                            "neutral", 0
                        ),

                        "Sad": emotions.get(
                            "sad", 0
                        ),

                        "Angry": emotions.get(
                            "angry", 0
                        ),

                        "Fear": emotions.get(
                            "fear", 0
                        ),

                        "Surprise": emotions.get(
                            "surprise", 0
                        ),

                        "Disgust": emotions.get(
                            "disgust", 0
                        ),

                        "UserNote": user_note,

                        "ImagePath": image_path
                    }

                    pd.DataFrame([record]).to_csv(
                        csv_path,
                        mode="a",
                        header=(
                            not os.path.exists(csv_path)
                            or os.path.getsize(csv_path) == 0
                        ),
                        index=False
                    )

                    st.success(
                        "✅ Snapshot Saved Successfully"
                    )

        # ------------------
        # RESET BUTTON
        # ------------------

        with col2:

            if st.button(
                "🔄 Reset Snapshot",
                use_container_width=True
            ):

                st.session_state.analyzed = False
                st.session_state.emotion_data = None
                st.session_state.captured_image = None

                st.rerun()

        

elif page == "📜 History":

    import pandas as pd
    import os

    st.title("📜 Emotion History")

    csv_path = "history/emotion_history.csv"

    if not os.path.exists(csv_path):

        st.warning("No history available.")

    else:

        df = pd.read_csv(csv_path)

        if len(df) == 0:

            st.warning("No saved snapshots.")

        else:

            emotion_filter = st.selectbox(
                "🎭 Filter Emotion",
                [
                    "All",
                    "Happy",
                    "Neutral",
                    "Sad",
                    "Angry",
                    "Fear",
                    "Surprise",
                    "Disgust"
                ]
            )

            if emotion_filter != "All":

                df = df[
                    df["DominantEmotion"]
                    == emotion_filter
                ]

            for index, row in df.iloc[::-1].iterrows():

                image_path = row.get(
                    "ImagePath",
                    ""
                )

                with st.container(border=True):

                    col1, col2 = st.columns([1, 2])

                    # --------------------
                    # IMAGE
                    # --------------------

                    with col1:

                        if (
                            image_path
                            and os.path.exists(
                                str(image_path)
                            )
                        ):

                            st.image(
                                image_path,
                                width=220
                            )

                    # --------------------
                    # DETAILS
                    # --------------------

                    with col2:

                        st.markdown(
                            f"### 🎭 {row['DominantEmotion']}"
                        )

                        st.caption(
                            f"📅 {row['Timestamp']}"
                        )

                        st.write("📝 Journal Note")

                        st.info(
                            row["UserNote"]
                        )

                        st.write("")

                        delete_col1, delete_col2 = st.columns([4, 1])

                        with delete_col2:

                            delete_clicked = st.button(
                                "🗑 Delete",
                                key=f"delete_{index}",
                                use_container_width=True
                            )

                        if delete_clicked:

                            if (
                                image_path
                                and os.path.exists(
                                    str(image_path)
                                )
                            ):

                                os.remove(
                                    image_path
                                )

                            df_original = pd.read_csv(
                                csv_path
                            )

                            df_original = (
                                df_original.drop(index)
                            )

                            df_original.to_csv(
                                csv_path,
                                index=False
                            )

                            st.success(
                                "✅ Snapshot deleted."
                            )

                            st.rerun()

                st.write("")


elif page == "📊 Analytics":

    import pandas as pd
    import os
    import matplotlib.pyplot as plt

    st.title("📊 Emotion Analytics Dashboard")

    csv_path = "history/emotion_history.csv"

    if not os.path.exists(csv_path):

        st.warning("No snapshot history found.")

    else:

        df = pd.read_csv(csv_path)

        if len(df) == 0:

            st.warning("No snapshots saved yet.")
            st.stop()

        # ======================
        # DATA PREPARATION
        # ======================

        df["Timestamp"] = pd.to_datetime(
            df["Timestamp"],
            errors="coerce"
        )

        df = df.dropna(
            subset=["Timestamp"]
        )

        df = df.sort_values(
            "Timestamp"
        )

        most_common = (
            df["DominantEmotion"]
            .value_counts()
            .idxmax()
        )

        # ======================
        # OVERVIEW CARDS
        # ======================

        st.subheader("📌 Overview")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Snapshots",
                len(df)
            )

        with col2:

            st.metric(
                "Most Common Emotion",
                most_common
            )

        with col3:

            st.metric(
                "Unique Emotions",
                df["DominantEmotion"].nunique()
            )

        # ======================
        # DISTRIBUTION
        # ======================

        st.divider()

        st.subheader(
            "📊 Emotion Distribution"
        )

        emotion_counts = (
            df["DominantEmotion"]
            .value_counts()
        )

        if emotion_counts.empty:

            st.warning(
                "No emotion data available."
            )

            st.stop()

        st.bar_chart(
            emotion_counts
        )

        # ======================
        # PIE CHART
        # ======================

        st.divider()

        st.subheader(
            "🥧 Emotion Breakdown"
        )

        fig, ax = plt.subplots()

        emotion_counts.plot(
            kind="pie",
            autopct="%1.1f%%",
            ax=ax
        )

        ax.set_ylabel("")

        st.pyplot(fig)

        # ======================
        # REAL EMOTION TIMELINE
        # ======================

        st.divider()

        st.subheader(
            "📈 Emotion Journey Over Time"
        )

        emotion_map = {
            "Angry": 1,
            "Disgust": 2,
            "Fear": 3,
            "Sad": 4,
            "Neutral": 5,
            "Happy": 6,
            "Surprise": 7
        }

        df["EmotionValue"] = (
            df["DominantEmotion"]
            .map(emotion_map)
        )

        timeline_df = df[
            [
                "Timestamp",
                "EmotionValue"
            ]
        ].set_index(
            "Timestamp"
        )

        st.line_chart(
            timeline_df
        )

        st.info(
            """
Emotion Scale

1 = Angry
2 = Disgust
3 = Fear
4 = Sad
5 = Neutral
6 = Happy
7 = Surprise
            """
        )

        # ======================
        # MULTI-EMOTION TREND
        # ======================

        st.divider()

        st.subheader(
            "🔥 Emotion Confidence Trends"
        )

        trend_df = df[
            [
                "Timestamp",
                "Happy",
                "Neutral",
                "Sad",
                "Angry",
                "Fear",
                "Surprise",
                "Disgust"
            ]
        ].set_index(
            "Timestamp"
        )

        st.line_chart(
            trend_df
        )

        st.caption(
            "Shows how each emotion confidence changes across saved snapshots."
        )

        # ======================
        # SNAPSHOT GALLERY
        # ======================

        st.divider()

        st.subheader(
            "📸 Recent Snapshots"
        )

        recent_df = df.tail(6)

        for _, row in recent_df.iterrows():

            image_path = row.get(
                "ImagePath",
                ""
            )

            if (
                image_path
                and os.path.exists(
                    str(image_path)
                )
            ):

                col1, col2 = st.columns(
                    [1, 2]
                )

                with col1:

                    st.image(
                        image_path,
                        width=150
                    )

                with col2:

                    st.write(
                        f"**Emotion:** {row['DominantEmotion']}"
                    )

                    st.write(
                        f"**Time:** {row['Timestamp']}"
                    )

                    if (
                        "UserNote"
                        in row
                    ):

                        st.info(
                            row["UserNote"]
                        )

                st.divider()

        # ======================
        # DOWNLOAD CSV
        # ======================

        st.divider()

        with open(
            csv_path,
            "rb"
        ) as f:

            st.download_button(
                "⬇ Download Emotion History CSV",
                f,
                file_name="emotion_history.csv"
            )

elif page == "📅 Reports":

    import pandas as pd
    import os
    from datetime import datetime, timedelta

    st.title("📅 Reports")
    st.caption(
    "Track emotional trends, mood patterns and personal reflections."
)
    csv_path = "history/emotion_history.csv"

    if not os.path.exists(csv_path):

        st.warning(
            "No emotion history found."
        )

    else:

        df = pd.read_csv(csv_path)

        if len(df) == 0:

            st.warning(
                "No entries available."
            )

        else:

            df["Timestamp"] = pd.to_datetime(
                df["Timestamp"],
                errors="coerce"
            )

            df = df.dropna(
                subset=["Timestamp"]
            )

            emotion_score_map = {
                "Happy": 100,
                "Surprise": 85,
                "Neutral": 70,
                "Sad": 40,
                "Fear": 35,
                "Disgust": 30,
                "Angry": 25
            }

            col1, col2 = st.columns([1,1])

            with col1:
                report_type = st.radio(
                    "", 
                    [
                        "📅 Daily Report",
                        "📈 Weekly Report"
                    ],
                    horizontal=True,
                    label_visibility="collapsed"
                )

            # ==================================
            # DAILY REPORT
            # ==================================

            if report_type == "📅 Daily Report":

                today = datetime.now().date()

                today_df = df[
                    df["Timestamp"].dt.date == today
                ]

                if len(today_df) == 0:

                    st.warning(
                        "No entries recorded today."
                    )

                else:

                    today_df["MoodScore"] = (
                        today_df["DominantEmotion"]
                        .map(emotion_score_map)
                    )

                    mood_score = (
                        today_df["MoodScore"]
                        .mean()
                    )

                    dominant_emotion = (
                        today_df["DominantEmotion"]
                        .value_counts()
                        .idxmax()
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "Mood Score",
                            f"{mood_score:.1f}/100"
                        )

                    with col2:

                        st.metric(
                            "Most Common Emotion",
                            dominant_emotion
                        )

                    st.divider()

                    with st.container(border=True):

                        st.subheader(
                            "🧠 Daily Insight"
                        )

                        if mood_score >= 80:

                            st.success(
                                "You seem to be having a very positive day."
                            )

                        elif mood_score >= 60:

                            st.info(
                                "Your emotional state appears balanced today."
                            )

                        elif mood_score >= 40:

                            st.warning(
                                "Your mood seems slightly low today."
                            )

                        else:

                            st.error(
                                "You seem stressed today. Focus on self-care."
                            )

                    st.divider()

                    st.subheader(
                        "📊 Today's Emotion Distribution"
                    )

                    emotion_counts = (
                        today_df["DominantEmotion"]
                        .value_counts()
                    )

                    st.bar_chart(
                        emotion_counts
                    )

                    st.divider()

                    st.subheader(
                        "📓 Today's Journal Entries"
                    )

                    for _, row in (
                        today_df.sort_values(
                            "Timestamp",
                            ascending=False
                        ).iterrows()
                    ):

                        note = row.get(
                            "UserNote",
                            ""
                        )

                        if pd.notna(note) and str(note).strip():

                            with st.expander(
                                f"🎭 {row['DominantEmotion']} • {row['Timestamp']}"
                            ):

                                st.write(note)

                        st.divider()

            # ==================================
            # WEEKLY REPORT
            # ==================================

            if report_type == "📈 Weekly Report":

                week_start = (
                    datetime.now().date()
                    - timedelta(days=6)
                )

                weekly_df = df[
                    df["Timestamp"].dt.date
                    >= week_start
                ]

                if len(weekly_df) == 0:

                    st.warning(
                        "No entries available this week."
                    )

                else:

                    weekly_df["MoodScore"] = (
                        weekly_df["DominantEmotion"]
                        .map(emotion_score_map)
                    )

                    weekly_score = (
                        weekly_df["MoodScore"]
                        .mean()
                    )

                    dominant_emotion = (
                        weekly_df["DominantEmotion"]
                        .value_counts()
                        .idxmax()
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "Weekly Mood Score",
                            f"{weekly_score:.1f}/100"
                        )

                    with col2:

                        st.metric(
                            "Most Common Emotion",
                            dominant_emotion
                        )

                    st.divider()

                    with st.container(border=True):

                        st.subheader(
                            "🧠 Weekly Insight"
                        )

                        if weekly_score >= 80:

                            st.success(
                                "Excellent emotional week."
                            )

                        elif weekly_score >= 60:

                            st.info(
                                "Overall balanced week."
                            )

                        elif weekly_score >= 40:

                            st.warning(
                                "Mixed emotional week."
                            )

                        else:

                            st.error(
                                "Challenging week emotionally."
                            )

                    st.divider()

                    st.subheader(
                        "📊 Weekly Emotion Distribution"
                    )

                    weekly_counts = (
                        weekly_df["DominantEmotion"]
                        .value_counts()
                    )

                    st.bar_chart(
                        weekly_counts
                    )

                    st.divider()

                    st.subheader(
                        "📈 Weekly Mood Trend"
                    )

                    trend_df = (
                        weekly_df.groupby(
                            weekly_df[
                                "Timestamp"
                            ].dt.date
                        )["MoodScore"]
                        .mean()
                    )

                    st.line_chart(
                        trend_df
                    )

                    st.divider()

                    st.subheader(
                        "📓 Weekly Journal Review"
                    )

                    recent_notes = (
                        weekly_df.sort_values(
                            "Timestamp",
                            ascending=False
                        )
                        .head(10)
                    )

                    for _, row in recent_notes.iterrows():

                        note = row.get(
                            "UserNote",
                            ""
                        )

                        if pd.notna(note) and str(note).strip():

                            with st.expander(
                                f"🎭 {row['DominantEmotion']} • {row['Timestamp']}"
                            ):

                                st.write(note)

                        st.divider()


elif page == "📄 PDF Report":

    import pandas as pd
    import os
    from datetime import datetime

    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        PageBreak
    )

    from reportlab.lib.styles import (
        getSampleStyleSheet
    )

    st.title("📄 EmotionSense AI Report")
    csv_path = "history/emotion_history.csv"

    if not os.path.exists(csv_path):

        st.warning(
            "No emotion history found."
        )

    else:

        df = pd.read_csv(csv_path)

        if len(df) == 0:

            st.warning(
                "No entries available."
            )

        else:

            st.success(
                f"{len(df)} entries found."
            )

            if st.button(
                "📄 Generate PDF Report"
            ):

                pdf_path = (
                    "EmotionSense_Report.pdf"
                )

                emotion_score_map = {
                    "Happy": 100,
                    "Surprise": 85,
                    "Neutral": 70,
                    "Sad": 40,
                    "Fear": 35,
                    "Disgust": 30,
                    "Angry": 25
                }

                df["MoodScore"] = (
                    df["DominantEmotion"]
                    .map(emotion_score_map)
                )

                average_score = (
                    df["MoodScore"]
                    .mean()
                )

                most_common = (
                    df["DominantEmotion"]
                    .value_counts()
                    .idxmax()
                )

                doc = SimpleDocTemplate(
                    pdf_path
                )

                styles = (
                    getSampleStyleSheet()
                )

                elements = []

                # ====================
                # COVER
                # ====================

                elements.append(
                    Paragraph(
                        "EmotionSense AI",
                        styles["Title"]
                    )
                )

                elements.append(
                    Paragraph(
                        "Emotion Analysis Report",
                        styles["Heading2"]
                    )
                )

                elements.append(
                    Spacer(1, 20)
                )

                elements.append(
                    Paragraph(
                        f"Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
                        styles["Normal"]
                    )
                )

                elements.append(
                    Spacer(1, 20)
                )

                # ====================
                # SUMMARY
                # ====================

                elements.append(
                    Paragraph(
                        "Summary",
                        styles["Heading1"]
                    )
                )

                elements.append(
                    Paragraph(
                        f"Total Entries: {len(df)}",
                        styles["Normal"]
                    )
                )

                elements.append(
                    Paragraph(
                        f"Most Common Emotion: {most_common}",
                        styles["Normal"]
                    )
                )

                elements.append(
                    Paragraph(
                        f"Average Mood Score: {average_score:.1f}/100",
                        styles["Normal"]
                    )
                )

                elements.append(
                    Spacer(1, 20)
                )

                # ====================
                # EMOTION COUNTS
                # ====================

                elements.append(
                    Paragraph(
                        "Emotion Distribution",
                        styles["Heading1"]
                    )
                )

                emotion_counts = (
                    df["DominantEmotion"]
                    .value_counts()
                )

                for emotion, count in (
                    emotion_counts.items()
                ):

                    elements.append(
                        Paragraph(
                            f"{emotion}: {count}",
                            styles["Normal"]
                        )
                    )

                elements.append(
                    Spacer(1, 20)
                )

                # ====================
                # RECENT ENTRIES
                # ====================

                elements.append(
                    Paragraph(
                        "Recent Mood Entries",
                        styles["Heading1"]
                    )
                )

                recent_entries = (
                    df.sort_values(
                        "Timestamp",
                        ascending=False
                    )
                    .head(10)
                )

                for _, row in (
                    recent_entries.iterrows()
                ):

                    elements.append(
                        Paragraph(
                            f"<b>{row['Timestamp']}</b>",
                            styles["Normal"]
                        )
                    )

                    elements.append(
                        Paragraph(
                            f"Emotion: {row['DominantEmotion']}",
                            styles["Normal"]
                        )
                    )

                    if (
                        "UserNote" in row
                        and pd.notna(
                            row["UserNote"]
                        )
                    ):

                        elements.append(
                            Paragraph(
                                f"Journal: {row['UserNote']}",
                                styles["Normal"]
                            )
                        )

                    elements.append(
                        Spacer(1, 10)
                    )

                elements.append(
                    PageBreak()
                )

                # ====================
                # FINAL INSIGHT
                # ====================

                elements.append(
                    Paragraph(
                        "Overall Insight",
                        styles["Heading1"]
                    )
                )

                if average_score >= 80:

                    insight = (
                        "The user has shown consistently positive emotional patterns."
                    )

                elif average_score >= 60:

                    insight = (
                        "The user has maintained a generally balanced emotional state."
                    )

                elif average_score >= 40:

                    insight = (
                        "The user experienced a mix of positive and negative emotional states."
                    )

                else:

                    insight = (
                        "The user appears to have experienced emotional challenges during this period."
                    )

                elements.append(
                    Paragraph(
                        insight,
                        styles["Normal"]
                    )
                )

                elements.append(
                    Spacer(1, 20)
                )

                elements.append(
                    Paragraph(
                        "Generated by EmotionSense AI",
                        styles["Italic"]
                    )
                )

                doc.build(
                    elements
                )

                st.success(
                    "PDF Generated Successfully!"
                )

                with open(
                    pdf_path,
                    "rb"
                ) as file:

                    st.download_button(
                        label="⬇ Download PDF",
                        data=file,
                        file_name="EmotionSense_Report.pdf",
                        mime="application/pdf"
                    )

elif page == "🏠 Home":

    # =====================================
    # CARD HOVER EFFECT
    # =====================================

    st.markdown("""
    <style>

    .feature-card{
        height:220px;
        padding:22px;
        border-radius:16px;
        border:1px solid rgba(255,255,255,0.12);
        background-color:rgba(255,255,255,0.02);
        transition:all 0.3s ease;
    }

    .feature-card:hover{
        transform:translateY(-6px);
        border:1px solid #3b82f6;
        box-shadow:0px 10px 30px rgba(59,130,246,0.20);
    }

    .feature-card h3{
        font-size:28px;
        margin-bottom:15px;
    }

    .feature-card p{
        color:#cbd5e1;
        font-size:16px;
        line-height:1.7;
    }

    </style>
    """, unsafe_allow_html=True)

    # =====================================
    # HERO SECTION
    # =====================================

    st.markdown("""
    <h1 style="
        font-size:60px;
        margin-bottom:0px;
    ">
    🧠 EmotionSense AI
    </h1>

    <h3 style="
        color:#94a3b8;
        margin-top:0px;
    ">
    Understand Your Emotions • Track Your Mood • Improve Your Well-Being
    </h3>
    """, unsafe_allow_html=True)

    st.info("""
    EmotionSense AI combines emotion recognition,
    mood journaling, personalized recommendations,
    productivity coaching, emotion history tracking,
    daily & weekly reports and PDF report generation
    into one intelligent platform.
    """)

    st.write("")

    # =====================================
    # QUICK ACTIONS
    # =====================================

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "📷 Upload Image",
            use_container_width=True
        ):

            st.session_state.page = "📷 Upload Image"
            st.rerun()

    with col2:

        if st.button(
            "📸 Snapshot Mode",
            use_container_width=True
        ):

            st.session_state.page = "📸 Snapshot Mode"
            st.rerun()

    with col3:

        if st.button(
            "📊 View Reports",
            use_container_width=True
        ):

            st.session_state.page = "📅 Reports"
            st.rerun()

    st.divider()

    # =====================================
    # FEATURE CARD FUNCTION
    # =====================================

    def feature_card(icon, title, description):

        st.markdown(f"""
        <div class="feature-card">

        <h3>{icon} {title}</h3>

        <p>{description}</p>

        </div>
        """, unsafe_allow_html=True)

    # =====================================
    # FEATURES
    # =====================================

    st.subheader("🚀 Key Features")

    st.write("")

    # ---------- ROW 1 ----------

    col1, col2, col3 = st.columns(3)

    with col1:
        feature_card(
            "📷",
            "Emotion Detection",
            "Analyze emotions from uploaded images and snapshots."
        )

    with col2:
        feature_card(
            "📓",
            "Mood Journal",
            "Save personal notes and build emotional awareness through journaling."
        )

    with col3:
        feature_card(
            "📊",
            "Reports",
            "Track daily and weekly emotional trends with detailed reports."
        )

    st.write("")

    # ---------- ROW 2 ----------

    col1, col2, col3 = st.columns(3)

    with col1:
        feature_card(
            "🎵",
            "Recommendations",
            "Receive emotion-based recommendations.ss."
        )

    with col2:
        feature_card(
            "🧠",
            "Productivity Coach",
            "Get productivity guidance based on your detected emotional state."
        )

    with col3:
        feature_card(
            "📄",
            "PDF Reports",
            "Generate downloadable emotion analysis reports with insights."
        )

    st.divider()

    # =====================================
    # WHY EMOTIONSENSE
    # =====================================

    st.subheader("✨ Why EmotionSense AI?")

    st.write("""
    EmotionSense AI goes beyond emotion detection.

    It combines emotion recognition, mood journaling,
    recommendations, productivity coaching, history tracking,
    reports and PDF generation into a single emotional
    intelligence platform.
    """)

    st.divider()

    st.caption(
        "Built with Streamlit • DeepFace • TensorFlow • OpenCV • Pandas • ReportLab"
    )

elif page == "🎯 Trained ResNet50 Model":

    st.title(
        "🎯 Trained ResNet50 Model"
    )

    st.caption(
        "Custom Emotion Recognition Model • Transfer Learning • FER2013"
    )

    st.divider()

    # ==================================
    # OVERVIEW
    # ==================================

    st.subheader(
        "📖 Model Overview"
    )

    with st.container(border=True):

        st.write("""
        This custom emotion recognition model was
        developed using the ResNet50 architecture
        and trained using Transfer Learning on the
        FER2013 facial emotion dataset.

        The objective was to accurately classify
        human emotions from facial expressions
        across seven emotion categories.
        """)

    # ==================================
    # MODEL DETAILS
    # ==================================

    st.divider()

    st.subheader(
        "⚙️ Model Configuration"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Architecture",
            "ResNet50"
        )

        st.metric(
            "Dataset",
            "FER2013"
        )

    with col2:

        st.metric(
            "Framework",
            "TensorFlow/Keras"
        )

        st.metric(
            "Technique",
            "Transfer Learning"
        )

    # ==================================
    # SUPPORTED EMOTIONS
    # ==================================

    st.divider()

    st.subheader(
        "😊 Supported Emotion Classes"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.success("😊 Happy")
        st.warning("😢 Sad")

    with col2:

        st.error("😠 Angry")
        st.info("😨 Fear")

    with col3:

        st.success("😲 Surprise")
        st.warning("🤢 Disgust")

    # ==================================
    # TRAINING PIPELINE
    # ==================================

    st.divider()

    st.subheader(
        "🔄 Training Pipeline"
    )

    with st.container(border=True):

        st.markdown("""
        **FER2013 Dataset**

        ⬇

        **Image Preprocessing**

        ⬇

        **ResNet50 Transfer Learning**

        ⬇

        **Model Training**

        ⬇

        **Emotion Classification**
        """)

    # ==================================
    # PERFORMANCE
    # ==================================

    st.divider()

    st.subheader(
        "📊 Model Performance"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Validation Accuracy",
            "92%"
        )

    with col2:

        st.metric(
            "Emotion Classes",
            "7"
        )

    st.write("")

    # --------------------------
    # ACCURACY CURVE
    # --------------------------

    with st.container(border=True):

        st.subheader(
            "📈 Accuracy Curve"
        )

        st.image(
            "assets/accuracy_curve.jpg",
            use_container_width=True
        )

    # --------------------------
    # LOSS CURVE
    # --------------------------

    with st.container(border=True):

        st.subheader(
            "📉 Loss Curve"
        )

        st.image(
            "assets/loss_curve.jpg",
            use_container_width=True
        )

    # --------------------------
    # CONFUSION MATRIX
    # --------------------------

    with st.container(border=True):

        st.subheader(
            "🎯 Confusion Matrix"
        )

        st.image(
            "assets/confusion_matrix.jpg",
            use_container_width=True
        )

    # ==================================
    # PRODUCTION SYSTEM
    # ==================================

    st.divider()

    st.subheader(
        "🚀 Production Deployment"
    )

    with st.container(border=True):

        st.info("""
        EmotionSense AI currently utilizes
        DeepFace for real-time emotion
        detection in production.

        The custom ResNet50 model represents
        the research, experimentation and
        model development component of the
        project.
        """)

    # ==================================
    # FUTURE WORK
    # ==================================

    st.divider()

    st.subheader(
        "🔮 Future Improvements"
    )

    with st.container(border=True):

        st.markdown("""
        - Deploy custom ResNet50 inference
        - Real-time prediction optimization
        - Explainable AI integration
        - Model benchmarking against DeepFace
        - Advanced emotion analytics
        """)

    st.divider()

    st.caption(
        "EmotionSense AI • Custom ResNet50 Research • DeepFace Production Engine"
    )