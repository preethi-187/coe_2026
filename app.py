import streamlit as st
try:
    import cv2
except ImportError:
    st.error("OpenCV is not installed properly. Please check requirements.txt")
    st.stop()
import numpy as np
from PIL import Image
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Document Scanner", layout="centered")

st.title("📄 Document Scanner App")
st.write("Upload a document image and convert it into a scanned PDF.")

uploaded_file = st.file_uploader(
    "Upload Document Image",
    type=["jpg", "jpeg", "png"]
)


def convert_to_scanned(image):
    # Convert PIL image to OpenCV format
    image_np = np.array(image)

    # Convert RGB to BGR
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    # Noise removal
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive threshold for scanner effect
    scanned = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return scanned


if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    if st.button("Convert to Scanned PDF"):

        scanned_image = convert_to_scanned(image)

        st.subheader("Scanned Black & White Image")
        st.image(scanned_image, channels="GRAY", use_container_width=True)

        # Save temporary scanned image
        temp_image_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name

        cv2.imwrite(temp_image_path, scanned_image)

        # Create PDF
        pdf = FPDF()
        pdf.add_page()

        pdf.image(temp_image_path, x=10, y=10, w=190)

        pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name

        pdf.output(pdf_path)

        # Download button
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="⬇ Download PDF",
                data=pdf_file,
                file_name="scanned_document.pdf",
        os.remove(temp_image_path)
