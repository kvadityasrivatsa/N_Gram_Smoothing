import re
import sys
import numpy as np
from nltk.tokenize import word_tokenize 

print(sys.argv)

n_gram = int(sys.argv[1])
smoothing_type = str(sys.argv[2])
path = str(sys.argv[3])

text = open(path, 'r').read()
text = re.sub('[^A-Za-z]+', ' ', text)
text = text.lower()
tokens = word_tokenize(text)

uni_list = []
bi_list = []
tri_list = []
quad_list = []

uni_count = {}
bi_count = {}
tri_count = {}
quad_count = {}

d = 0.75

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

#4A
for i in range(int(len(tokens))-3):
	quad = tokens[i]+" "+tokens[i+1]+" "+tokens[i+2]+" "+tokens[i+3]
	quad_list.append(quad)
	i+=4

#4B
for quad in quad_list:
	if(quad not in quad_count):
		quad_count[quad]=1
	else:
		quad_count[quad]+=1
# print(quad_count)
# print("//////////////////")

def count(string):
	n = len(string.split()) 
	val = 0
	if(n==3):
		if(string in tri_count):
			val = tri_count[string]
	elif(n==2):
		if(string in bi_count):
			val = bi_count[string]
	elif(n==1):
		if(string in uni_count):
			val = uni_count[string]
	return val


def countck(string):
	n = len(string.split()) 
	val = 0
	if(n==3):
		for x in uni_count:
			if(x+" "+string in quad_count):
				val+=1
		return val
	elif(n==2):
		for x in uni_count:
			if(x+" "+string in tri_count):
				val+=1
		return val
	elif(n==1):
		for x in uni_count:
			if(x+" "+string in bi_count):
				val+=1
		return val
	else:
		return 0

def lam(string):
	n = len(string.split())
	num = 0
	den = 0
	print(string)
	for w in uni_count:
		if(string!=""):
			if(countck(string+" "+w)>0):
				num+=1
		else:
			if(countck(w)>0):
				num+=1
	print("num=",num)

	if(string!=""):
		for v in uni_count:
			den+=countck(string+" "+v)
	else:
		for v in uni_count:
			den+=countck(v)		
	print("den=",den)

	if(num==0 and den!=0):
		# print("WTF")
		return d/float(den)
	elif(den==0):
		print("WTF")
		return 0
	else:
		return d*float(num)/float(den)

def max(x,y):
	if(x>y):
		return x
	else:
		return y

def tri_pkn_prim(string):
	string_list = string.split()
	word = string_list[2]
	context = string_list[0]+" "+string_list[1]
	num1 = max(count(string)-d,0)
	den1 = 0
	for v in uni_count:
		den1+=count(context+" "+v)
	if(num1==0 or den1==0):
		return lam(context)*bi_pkn_aux(string_list[1]+" "+string_list[2])
	else:
		return float(num1)/float(den1) + lam(context)*bi_pkn_aux(string_list[1]+" "+string_list[2])

def bi_pkn_aux(string):
	string_list = string.split()
	word = string_list[1]
	context = string_list[0]
	num1 = max(countck(string)-d,0)
	den1 = 0
	for v in uni_count:
		den1+=countck(context+" "+v)
	if(num1==0 or den1==0):
		return lam(context)*uni_pkn_aux(string_list[1])
	else:
		return float(num1)/float(den1) + lam(context)*uni_pkn_aux(string_list[1])

def uni_pkn_aux(string):	# string : single word
	word = string
	num1 = max(countck(string)-d,0)
	den1 = 0
	for v in uni_count:
		den1+=countck(v)
	if(num1==0 or den1==0):
		return lam("")/len(uni_count)
	else: 
		return float(num1)/float(den1) + lam("")/len(uni_count) # len(uni_count) = V

def bi_pkn_prim(string):
	string_list = string.split()
	word = string_list[1]
	context = string_list[0]
	num1 = max(count(string)-d,0)
	den1 = 0
	for v in uni_count:
		den1+=count(context+" "+v)
	if(num1==0 or den1==0):
		return lam(context)*uni_pkn_aux(string_list[1])
	else:
		return float(num1)/float(den1) + lam(context)*uni_pkn_aux(string_list[1])

def uni_pkn_prim(string):	# string : single word
	word = string
	num1 = max(count(string)-d,0)
	den1 = 0
	for v in uni_count:
		den1+=count(v)
	if(num1==0 or den1==0):
		print("num1 & den1 =0")
		return lam("")/len(uni_count)
	else: 
		return float(num1)/float(den1) + lam("")/len(uni_count) # len(uni_count) = V


def trigram_main_func(string):	# string is a sentence
	string_list = string.split()
	prod = 1
	for i in range(len(string_list)-2):
		aux_prob = tri_pkn_prim(string_list[i]+" "+string_list[i+1]+" "+string_list[i+2])	# window size = 3
		prod*=aux_prob
	i+=1
	return prod

def bigram_main_func(string):	# string is a sentence
	string_list = string.split()
	prod = 1
	for i in range(len(string_list)-1):
		aux_prob = bi_pkn_prim(string_list[i]+" "+string_list[i+1])	# window size = 2
		prod*=aux_prob
	i+=1
	return prod

def unigram_main_func(string):	# string is a sentence
	string_list = string.split()
	prod = 1
	for i in range(len(string_list)):
		aux_prob = uni_pkn_prim(string_list[i])	# window size = 1
		prod*=aux_prob
	i+=1
	return prod

# print(sorted(uni_count))

# for w in sorted(uni_count, key=uni_count.get, reverse=True):
#   print(w, uni_count[w])

# for w in sorted(bi_count, key=bi_count.get, reverse=True):
#   print(w, bi_count[w])

# for w in sorted(tri_count, key=tri_count.get, reverse=True):
#   print(w, tri_count[w])

# for w in sorted(quad_count, key=quad_count.get, reverse=True):
#   print(w, quad_count[w])


# print(count("boy"))
# print(countck("boy"))
# print("MAKE")
# print(lam("make"))

# print(tri_pkn_prim("the procreant earth"))

# print(trigram_main_func("urge and urge and urge"))
# print(bigram_main_func("urge and urge and urge"))
# print(unigram_main_func("urge and urge and urge"))

# text = re.sub('[^A-Za-z]+', ' ', text)
# text = text.lower()

sent = input("input sentence:")
sent = re.sub('[^A-Za-z]+', ' ', sent)
sent = sent.lower()

if(n_gram==3):
	print(trigram_main_func(sent))
elif(n_gram==2):
	print(bigram_main_func(sent))
elif(n_gram==1):
	print(unigram_main_func(sent))