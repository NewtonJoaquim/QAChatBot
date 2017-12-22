from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

stpw = stopwords.words('portuguese')

def find_tags(text):
    text_no_punctuation = "".join(w for w in text if w not in string.punctuation)
    tokens = word_tokenize(text_no_punctuation)
    tokens = [w.lower() for w in tokens]
    tokens = [w for w in tokens if w not in stpw]
    return tokens

print(find_tags("Quem foi D. Pedro I?"))