import streamlit as st
from PIL import Image
import cv2
import numpy as np
import tempfile
import os

st.title("🎬📸 Smart Media Analyzer")

uploaded_file = st.file_uploader(
    "Upload an Image or Video",
    type=["jpg", "jpeg", "png", "mp4"]
)

if uploaded_file:
    file_type = uploaded_file.type

    if "image" in file_type:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        width, height = image.size
        size_kb = len(uploaded_file.getvalue()) / 1024

        st.write(f"Width: {width}px")
        st.write(f"Height: {height}px")
        st.write(f"File Size: {size_kb:.2f} KB")

    elif "video" in file_type:
        st.video(uploaded_file)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        cap = cv2.VideoCapture(temp_path)

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps if fps > 0 else 0

        st.write(f"Frame Count: {frame_count}")
        st.write(f"FPS: {fps:.2f}")
        st.write(f"Duration: {duration:.2f} seconds")

        success, frame = cap.read()
        if success:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            st.image(frame_rgb, caption="Video Thumbnail", use_container_width=True)

        cap.release()
        os.remove(temp_path)
