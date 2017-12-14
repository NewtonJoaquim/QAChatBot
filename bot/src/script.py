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

    return loaded_model, loaded_model_vocab

def predict(model, vocab, data):
    vectorizer = CountVectorizer(vocabulary=vocab)
    data_v = []
    data_v.append(data)
    predict_vect = vectorizer.transform(data_v)
    predictions = model.predict(predict_vect)
    return predictions

model, vocab = initialize_model()

file = open('testfile.txt','w') 

data_to_send = predict(model, vocab, sys.argv[1])
file.write(sys.argv[1]) 
print(data_to_send[0])
sys.stdout.flush()
