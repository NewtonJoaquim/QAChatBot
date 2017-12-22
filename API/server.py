from flask import Flask, jsonify, request, url_for
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from flask_cors import CORS
import os, json, re 
import pandas as pd

app = Flask(__name__)
CORS(app)

def initialize_model():
    #PATH = os.path.abspath('..\model')
    PATH = os.path.abspath('..\model')
    filename = PATH + '\modelQA.pkl'
    with open(filename ,'rb') as f:
        loaded_model = joblib.load(f) 

    vocab_filename = PATH + '\modelQA_vocabulary.pkl'
    with open(vocab_filename ,'rb') as f:
        loaded_model_vocab = joblib.load(f) 

    return loaded_model, loaded_model_vocab

model, vocab = initialize_model()

@app.route("/answer", methods=['POST'])
def predict_answer():

    vectorizer_train = CountVectorizer(vocabulary=vocab)
    req_data = request.get_json()
    teste_predict = []
    req_array = req_data['data']
    for i in range(len(req_array)):
        desc = req_array[i]['question']
        teste_predict.append(desc)
       
    teste_predict_vect = vectorizer_train.transform(teste_predict) 
    predictions = model.predict(teste_predict_vect)
 
    pred_prob_list = model.predict_proba(teste_predict_vect).tolist()

    output_json = json_concatenation(req_data,'data', predictions.tolist())

    return output_json

def json_concatenation(input_json, json_key, predictions_list):
    teste_predict = input_json[json_key]
    output_dict= []
    for i in range(len(predictions_list)):
        data = {
            "answer": predictions_list[i]
        } 
        output_dict.append(data)
            
    output_json = {"data" : output_dict}
    return jsonify(output_json)

app.run()