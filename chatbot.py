from streamlit_chat import message
from st_clickable_images import clickable_images
from PIL import Image
from helper import *

import streamlit as st

def init_chat_history():
    if 'question' not in st.session_state:
        st.session_state['question'] = []

    if 'answer' not in st.session_state:
        st.session_state['answer'] = []


def update_chat_messages():
    if st.session_state['answer']:
        for i in range(len(st.session_state['answer'])-1, -1, -1):
            message(st.session_state['answer'][i], key=str(
                i), avatar_style='bottts', seed=123)
            message(st.session_state['question'][i], avatar_style='micah', seed=45,
                    is_user=True, key=str(i) + '_user')


def predict(image, input):
    if image is None or not input:
        return

    with st.spinner('Preparing answer...'):
        answer = request_answer(st.session_state.uploaded_image, input)
        st.session_state.question.append(input)
        st.session_state.answer.append(answer)
        while len(st.session_state.question) >= 5:
            st.session_state.answer.pop(0)
            st.session_state.question.pop(0)


def upload_image_callback():
    st.session_state.uploaded_image = upload_image_to_server()
    st.session_state.question = []
    st.session_state.answer = []
    st.session_state.input = ''


def show():
    init_chat_history()

    st.title('Welcome to Visual Question Answering - Chat AI')
    st.markdown('''
            <h4 style='text-align: center; color: #B2BEB5;'>
            <i>Hi, I am a Visual conversational AI, capable of answering a sequence of questions about images.
                Please upload image and fire away!
            </i></h4>
            ''', unsafe_allow_html=True)

    update_gallery_images()
    if 'gallery' in st.session_state:
        clicked = clickable_images(
            st.session_state.gallery,
            titles=[f"Image #{str(i)}" for i in range(2)],
            div_style={"display": "flex",
                       "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "height": "100px"},
        )

        if 'clicked' not in st.session_state or st.session_state.clicked != clicked:
            st.session_state.uploaded_image = st.session_state.gallery_images[clicked]
            st.session_state.clicked = clicked
            st.session_state.question = []
            st.session_state.answer = []
            st.session_state.input = ''

    image_col, text_col = st.columns(2)
    with image_col:
        st.file_uploader('Select an image...', type=[
            'jpg', 'jpeg'], accept_multiple_files=False,
            on_change=upload_image_callback, key='uploader')

        if st.session_state.uploaded_image is not None:
            image = Image.open(st.session_state.uploaded_image)
            st.image(st.session_state.uploaded_image,
                     use_column_width='always')
        else:
            st.session_state.question = []
            st.session_state.answer = []
            st.session_state.input = ''

    with text_col:
        input = st.text_input('Enter question: ', '', key='input')
        if input:
            predict(image, input)
        update_chat_messages()
