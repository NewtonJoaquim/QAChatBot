from flask import Flask, jsonify, request, url_for
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from flask_cors import CORS
import os, json, re, time 
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

    context_filename = PATH + '\modelQA_context.pkl'
    with open(context_filename ,'rb') as f:
        loaded_model_context = joblib.load(f) 

    context_vocab_filename = PATH + '\modelQA_context_vocabulary.pkl'
    with open(context_vocab_filename ,'rb') as f:
        loaded_model_vocab_context = joblib.load(f)

    return loaded_model, loaded_model_vocab, loaded_model_context, loaded_model_vocab_context

model, vocab, model_c, vocab_c = initialize_model()

@app.route("/answer", methods=['POST'])
def predict_answer():

    start_time = time.time()
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
    print("answer time: " + str(time.time() - start_time))
    print("answer probability:" + str(get_greatest_probabilities(pred_prob_list)))
    output_json = json_concatenation(req_data,'data', predictions.tolist())

    return output_json

@app.route("/context", methods=['POST'])
def predict_context():

    start_time = time.time()
    vectorizer_train = CountVectorizer(vocabulary=vocab_c)
    req_data = request.get_json()
    teste_predict = []
    req_array = req_data['data']
    for i in range(len(req_array)):
        desc = req_array[i]['question']
        teste_predict.append(desc)

    teste_predict_vect = vectorizer_train.transform(teste_predict) 
    predictions = model_c.predict(teste_predict_vect)
 
    pred_prob_list = model_c.predict_proba(teste_predict_vect).tolist()
    print("context time: " + str(time.time() - start_time))
    print("context probability:" + str(get_greatest_probabilities(pred_prob_list)))
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

def get_greatest_probabilities(pred_prob_list):
    max_probabilities = []
    for i in pred_prob_list:
       max_probabilities.append(max(i))
    return max_probabilities

app.run()