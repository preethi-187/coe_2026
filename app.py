import streamlit as st
from PIL import Image
import cv2
import numpy as np
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Document Scanner", layout="centered")

st.title("📄 Document Scanner App")
st.write("Upload a document image, convert it into black & white scan, and download it as PDF.")

uploaded_file = st.file_uploader("Upload Document Image", type=["jpg", "jpeg", "png"])


def convert_to_scan(image):
    # Convert PIL image to OpenCV format
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Noise removal
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive threshold for scanned effect
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

    if st.button("Convert to Black & White Scan"):
        scanned_image = convert_to_scan(image)

        st.subheader("Scanned Image")
        st.image(scanned_image, channels="GRAY", use_container_width=True)

        # Save scanned image temporarily
        temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        cv2.imwrite(temp_img.name, scanned_image)

        # Create PDF
        pdf = FPDF()
        pdf.add_page()

        # Fit image to page
        pdf.image(temp_img.name, x=10, y=10, w=190)

        pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(pdf_path.name)

        # Download button
        with open(pdf_path.name, "rb") as f:
            st.download_button(
                label="📥 Download PDF",
                data=f,
                file_name="scanned_document.pdf",
                mime="application/pdf"
            )

        # Cleanup
        os.unlink(temp_img.name)
