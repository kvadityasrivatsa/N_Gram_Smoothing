import re
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize 

text = open('mini_corpus.txt', 'r').read()
# text = re.sub(r'[,.;:]', ' ', text)
text = re.sub('[^A-Za-z]+', ' ', text)
text = text.lower()
# print(text)
tokens = word_tokenize(text)
unigram_count = {}
bigram_count = {}


for word in tokens:
	if(word not in unigram_count):
		unigram_count[word]=1
	else:
		unigram_count[word]+=1

# print(unigram_count)
# print(sorted(unigram_count))

for w in sorted(unigram_count, key=unigram_count.get, reverse=True):
  print(w, unigram_count[w])


