from transformers import ViltProcessor
from transformers import ViltForQuestionAnswering
from joblib import load


import os
import re
import string
import torch
import pandas as pd

'''
Visual Question Answering Model to generate answer statement for
question.
'''


class Predictor:
    def __init__(self):
        auth_token = os.environ.get('TOKEN') or True
        self.vqa_processor = ViltProcessor.from_pretrained(
            'tufa15nik/vilt-finetuned-vqasi')
        self.vqa_model = ViltForQuestionAnswering.from_pretrained(
            'tufa15nik/vilt-finetuned-vqasi')
        # self.qa_model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
        # self.qa_tokenizer = AutoTokenizer.from_pretrained("t5-small")
        # self.qa_model = AutoModelForSeq2SeqLM.from_pretrained(
        #     'Madhuri/t5_small_vqa_fs',  use_auth_token=auth_token)
        # self.qa_tokenizer = AutoTokenizer.from_pretrained(
        #     'Madhuri/t5_small_vqa_fs', use_auth_token=auth_token)
        # self.happy_tt = HappyTextToText(
        #     "T5", "vennify/t5-base-grammar-correction")
        # self.tt_args = TTSettings(num_beams=5, min_length=1)
        model_path= os.path.join( os.path.dirname(os.path.abspath(__file__)), 'qa_classifier.joblib')
        self.qa_classifier = load(model_path)

    def is_valid_question(self, question):
        df=pd.DataFrame()
        df['sentence']=[question]
        return self.qa_classifier.predict(df['sentence'])[0] == 1

    def predict_answer_from_text(self, image, input):
        if image is None:
            return 'Please select an image and ask a question...'

        chars = re.escape(string.punctuation)
        question = re.sub(r'['+chars+']', '', input)
        if not question or len(question.split()) < 3:
            return 'I cannot understand, please ask a valid question...'

        if not self.is_valid_question(question):
            return 'I can understand only questions, can you please ask a valid question...'

        # process question using image model
        encoding = self.vqa_processor(image, question, return_tensors='pt')
        with torch.no_grad():
            outputs = self.vqa_model(**encoding)
        answer = self.vqa_model.config.id2label[outputs.logits.argmax(
            -1).item()]

        return answer
