from os import listdir
from os.path import *
from PIL import Image
from io import BytesIO

import streamlit as st
import base64
import requests


def update_gallery_images():
    if 'gallery' not in st.session_state:
        st.session_state['gallery'] = []
        st.session_state['gallery_images'] = []
        image_path = join(dirname(abspath(__file__)), 'images')
        for f in listdir(image_path):
            if f.startswith('image'):
                with open(join(image_path, f), "rb") as image:
                    encoded = base64.b64encode(image.read()).decode()
                    st.session_state.gallery.append(
                        f"data:image/jpeg;base64,{encoded}")
                    st.session_state.gallery_images.append(join(image_path, f))


def upload_image_to_server():
    if st.session_state.uploader is not None:
        image = Image.open(st.session_state.uploader)
        byte_io = BytesIO()
        image.save(byte_io, 'png')
        byte_io.seek(0)
        file = {'file': byte_io}
        response = requests.post('http://0.0.0.0:8080/uploadfile/', files=file)
        if response.status_code == 200:
            return response.json()['filename']
    return None


def request_answer(image, question):
    response = requests.get(
        f'http://0.0.0.0:8080/vqa?image={image}&question={question}')
    if response.status_code == 200:
        return response.json()['answer']
    return 'I do not understand. Please ask again.'
