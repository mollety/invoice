from dotenv import load_dotenv

load_dotenv()  #Loading all environmental variables from .env

import streamlit as st
import os

from PIL import Image

import google.generativeai as genai

genai.configure(api_key= os.getenv("GOOGLE_API_KEY"))



##Code to load gemini pro vision

model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input, image, prompt):
    response= model.generate_content([input, image[0], prompt])
    return response.text 

def image_input_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts

    else:
        raise FileNotFoundError("No File Uploaded")



## initialize streamli application
st.set_page_config(page_title="Invoice Extractor")
st.header("Invoice Extractor")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image of the Invoice ..... ", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Tax Invoice", use_column_width= True)

submit = st.button("Tell me about invoice")

input_prompt = """
You are expert in understanding invoice , we will upload image as invoices 
and you will have to answer any questions based on the uploaded invoice images
"""

#if submit button is clicked

if submit:
    image_data = image_input_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The response is ")
    st.write(response)