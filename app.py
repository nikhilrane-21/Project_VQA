import uvicorn
import streamlit as st
from multiprocessing import Process

import socket
import time
import chatbot
import os


def run_st_app():
    st.set_page_config(
        page_title='Welcome to Visual Question Answering - AI',
        page_icon=':robot:',
        layout='wide'
    )

    st.sidebar.title('VQA AI')
    st.sidebar.write('''
        VQA conversational AI addresses the challenge of visual question answering with the chat assistance.
        Here, we fine-tuned ViLT(Vision-and-Language Transformer) model on VQA with satellite images. 
        We pretrained and finetuned our model on Language transformer to get the desired result.
        
        Sample Questions you can try:
        
        --> Does this picture contain trees?
        --> How many trees in the picture?
        --> How many boats in the picture?
        --> How many cars in the picture?
        --> How many red cars in the picture?
        --> how many residential buildings are there?
        --> How many buildings in the picture?
        --> what is the number of water areas?
        --> how many pitchs are there?
        --> is there a water area present?
        --> is there a parking?
        --> how many vehicles are there in this picture?
        --> does this picture contain plane?
        --> does this picture contain small vehicle?
        --> does this picture contain large vehicle?
        --> does this picture contain tennis court?
        --> What is the overall condition of the given image?
        --> How many non flooded buildings can be seen in this image?
        --> How many buildings can be seen in the image?
        --> Is the entire road non flooded?
        --> Is the entire road flooded?
        --> What is the condition of the road in this image?
        --> How many buildings are non flooded in this image?
        --> How many buildings are flooded in this image?
        --> How many flooded buildings can be seen in this image?
        ''')

    chatbot.show()




def run_uvicorn():
    os.system('uvicorn server:app --port 8080 --host 0.0.0.0 --workers 1')


def start_server():
    if not is_port_in_use(8080):
        with st.spinner(text='Loading models...'):
            proc = Process(target=run_uvicorn, args=(), daemon=True)
            proc.start()
            while not is_port_in_use(8080):
                time.sleep(1)
            st.success('Models are loaded.')


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('0.0.0.0', port)) == 0


if __name__ == '__main__':
    run_st_app()
    if 'server' not in st.session_state:
        st.session_state['server'] = True
        start_server()

