from fastapi import FastAPI, File, UploadFile
from model import predictor
from os import listdir
from os.path import *
from PIL import Image

import os
import hashlib
import threading
import time

gpredictor = None
app = FastAPI()

@app.get('/')
def root():
    return {'app': 'Thanks for visiting!!'}


@app.get('/favicon.ico', include_in_schema=False)
@app.post('/uploadfile/')
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    hash = hashlib.sha256(contents).hexdigest()
    file.filename = f'images/upload_{hash}.jpg'
    if not os.path.isfile(file.filename):
        with open(file.filename, 'wb') as f:
            f.write(contents)
    images[file.filename] = Image.open(file.filename)
    return {'filename': file.filename}


@app.get('/vqa')
async def answer(
    image: str,
    question: str
):
    if image not in images:
        print('not in image')
        pil_image = Image.open(image)
        images[image] = pil_image
    else:
        pil_image = images[image]
    while gpredictor is None:
        time.sleep(1)
    answer = gpredictor.predict_answer_from_text( pil_image, question )
    return {'answer': answer }

os.environ['TOKENIZERS_PARALLELISM'] = 'false'
images={}

def runInThread():
    collect_images()
    print('Initialize model in thread')
    global gpredictor
    gpredictor = predictor.Predictor()
    print('Model is initialized')


def collect_images():
    image_path = join(dirname(abspath(__file__)), 'images')
    for f in listdir(image_path):
        if f.startswith('image'):
            full_image_path = join(image_path, f)
            images[full_image_path] = Image.open(full_image_path)

thread = threading.Thread(target=runInThread)
thread.start()