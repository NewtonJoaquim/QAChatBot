
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import re
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib


# In[2]:


df = pd.read_csv("QAdata.csv",sep="|")
df


# In[3]:


y = df.resposta
y2 = df.contexto
X = df.pergunta

# In[4]:


vectorizer_train = CountVectorizer(ngram_range=(1, 10))
X = vectorizer_train.fit_transform(X)


# In[5]:


model = MultinomialNB()
model.fit(X,y)

model_context = MultinomialNB()
model_context.fit(X, y2)

teste_predict_vect = vectorizer_train.transform(['por que independencia'])
model.predict(teste_predict_vect)


# ### Exportando o modelo gerado

# In[6]:


filename = 'modelQA.pkl'
with open (filename, 'wb') as file:
    joblib.dump(model, file)
    
file.close()

filename = 'modelQA_vocabulary.pkl'
with open (filename, 'wb') as file:
    joblib.dump(vectorizer_train.vocabulary_, file)
    
file.close()

filename = 'modelQA_context.pkl'
with open (filename, 'wb') as file:
    joblib.dump(model_context, file)
    
file.close()

filename = 'modelQA_context_vocabulary.pkl'
with open (filename, 'wb') as file:
    joblib.dump(vectorizer_train.vocabulary_, file)
    
file.close()
