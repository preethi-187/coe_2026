import streamlit as st
from PIL import Image

st.title("🖼️ Image Analyzer")

uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Image", use_container_width=True)

    width, height = image.size
    file_size = len(uploaded_file.getvalue()) / 1024  # KB

    st.subheader("📊 Image Details")
    st.write(f"📏 Width: {width} pixels")
    st.write(f"📐 Height: {height} pixels")
    st.write(f"💾 File Size: {file_size:.2f} KB")
    st.write(f"🖼️ Format: {image.format}")
    st.write(f"🎨 Color Mode: {image.mode}")
