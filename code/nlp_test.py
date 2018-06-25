import numpy as np
import pandas as pd
import nltk
from bs4 import BeautifulSoup
import urllib.request

response = urllib.request.urlopen('http://php.net')
html = response.read()
soup = BeautifulSoup(html, 'html5lib')
text = soup.get_text(strip=True)
# print(text)
tokens = [t for t in text.split()]
print(tokens)
from nltk.corpus import stopwords
clean_tokens = tokens[:]
for token in tokens:
    if token in stopwords.words('english'):
        clean_tokens.remove(token)

freq = nltk.FreqDist(clean_tokens)
# for key, val in freq.items():
#     print(str(key) + ':' + str(val))
freq.plot(20, cumulative=False)
from nltk.corpus import wordnet
print(wordnet.synset('dog.n.01').definition())
