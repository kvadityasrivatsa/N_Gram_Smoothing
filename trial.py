import re
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize 

text = open('corpus.txt', 'r').read()
text = re.sub('[^A-Za-z]+', ' ', text)
text = text.lower()
tokens = word_tokenize(text)
uni_list = []
bi_list = []
tri_list = []
uni_count = {}
bi_count = {}
tri_count = {}

#1A
for i in range(len(tokens)):
	uni = tokens[i]
	uni_list.append(uni)
	i+=1

#1B
for uni in uni_list:
	if(uni not in uni_count):
		uni_count[uni]=1
	else:
		uni_count[uni]+=1
# print(uni_count)
# print("//////////////////")

#2A
for i in range(int(len(tokens))-1):
	bi = tokens[i]+" "+tokens[i+1]
	bi_list.append(bi)
	i+=2

#2B
for bi in bi_list:
	if(bi not in bi_count):
		bi_count[bi]=1
	else:
		bi_count[bi]+=1
# print(bi_count)
# print("//////////////////")

#3A
for i in range(int(len(tokens))-2):
	tri = tokens[i]+" "+tokens[i+1]+" "+tokens[i+2]
	tri_list.append(tri)
	i+=3

#3B
for tri in tri_list:
	if(tri not in tri_count):
		tri_count[tri]=1
	else:
		tri_count[tri]+=1
# print(tri_count)
# print("//////////////////")



# print(sorted(unigram_count))

# for w in sorted(unigram_count, key=unigram_count.get, reverse=True):
#   print(w, unigram_count[w])


