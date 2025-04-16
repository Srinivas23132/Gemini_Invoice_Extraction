# invoice_extractor.py

import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if the API key is available
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found in .env file. Please add it.")
    st.stop()

# Configure the Google Generative AI API key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model using 'gemini-2.0-flash'
try:
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error(f"Error initializing the Gemini model: {e}")
    st.stop()

st.title("Invoice Data Extractor")

# Prompt input for the invoice extraction requirements
prompt = st.text_input("Enter your prompt (e.g., 'Extract total amount, invoice number, and date')")

# Invoice image file uploader (accepts jpg, jpeg, png formats)
uploaded_image = st.file_uploader("Upload an invoice image", type=["jpg", "jpeg", "png"])

if uploaded_image and prompt:
    # Open and display the uploaded image using the new parameter
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Invoice", use_container_width=True)

    # Instead of converting the image to bytes, pass the PIL image directly to the model.
    try:
        response = model.generate_content([prompt, image])
        st.subheader("Extracted Information:")
        st.write(response.text)
    except Exception as e:
        st.error(f"Error generating response: {e}")
