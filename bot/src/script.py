import os, sys, time
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer


def initialize_model():
    PATH = os.path.abspath('..\..\model')
    filename = PATH + '\modelQA.pkl'
    with open(filename ,'rb') as f:
        loaded_model = joblib.load(f) 

    vocab_filename = PATH + '\modelQA_vocabulary.pkl'
    with open(vocab_filename ,'rb') as f:
        loaded_model_vocab = joblib.load(f) 

    context_filename = PATH + '\modelQA_context.pkl'
    with open(filename ,'rb') as f:
        loaded_model_context = joblib.load(f) 

    context_vocab_filename = PATH + '\modelQA_context_vocabulary.pkl'
    with open(vocab_filename ,'rb') as f:
        loaded_model_vocab_context = joblib.load(f) 

    return loaded_model, loaded_model_vocab, loaded_model_context, loaded_model_vocab_context

def predict(model, vocab, data):
    vectorizer = CountVectorizer(vocabulary=vocab)
    data_v = []
    data_v.append(data)
    predict_vect = vectorizer.transform(data_v)
    predictions = model.predict(predict_vect)
    return predictions

def predict_context(model,vocab, data):
    predict(model,vocab,data)

model, vocab, model_c, vocab_c = initialize_model()

file = open('testfile.txt','w') 

data_to_send = predict(model, vocab, sys.argv[1])
context_to_send = predict_context(model_c, vocab, sys.argv[1])
file.write(sys.argv[1]) 
print(data_to_send[0])
sys.stdout.flush()
