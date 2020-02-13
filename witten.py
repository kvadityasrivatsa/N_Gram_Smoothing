import re
import sys
from nltk.tokenize import word_tokenize 

def fetchNclean(path):
	text = open(path, 'r').read()
	text = re.sub('[^A-Za-z]+', ' ', text)
	text = text.lower()
	global tokens
	tokens = word_tokenize(text)

uni_list = []
bi_list = []
tri_list = []
quad_list = []

uni_count = {}
bi_count = {}
tri_count = {}
quad_count = {}

gram = 3

def prep_ds(n):

	global tokens
	global uni_list
	global uni_count
	global bi_list
	global bi_count
	global tri_list
	global tri_count
	global V

	global gram
	gram = n

	#1A
	for i in range(len(tokens)):
		uni = tokens[i]
		uni_list.append(uni)

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

	#3B
	for tri in tri_list:
		if(tri not in tri_count):
			tri_count[tri]=1
		else:
			tri_count[tri]+=1
	print(tri_count)
	print("//////////////////")

	V = len(uni_count)


def count(string):
	n = len(string.split()) 
	if(n==3 and string in tri_count):
		return tri_count[string]
	elif(n==2 and string in bi_count):
		return bi_count[string]
	elif(n==1 and string in uni_count):
		return uni_count[string]
	else:
		return 0

def Pwb3(string):
	vect = string.split()
	word = vect[2]
	context = vect[0] + " " + vect[1]
	T = 0
	for w in uni_count:
		if(context+" "+w in tri_count):
			T+=1
	N = 0
	for v in uni_count:
		if(context+" "+v in tri_count):
			N+=tri_count[context+" "+v]
	Z = V - T

	print("Pwb3: string=",string,"T=",T,"N=",N,"Z=",Z,"CNT=",count(string))

	if(T==0 and N==0):
		return 0
	elif(count(string)>0):
		return count(string)/(N+T)
	else:
		return T/(Z*(T+N))

def Pwb2(string):
	vect = string.split()
	word = vect[1]
	context = vect[0]
	T = 0
	for w in uni_count:
		if(context+" "+w in bi_count):
			T+=1
	N = 0
	for v in uni_count:
		if(context+" "+v in bi_count):
			N+=bi_count[context+" "+v]
	Z = V - T

	print("Pwb2: string=",string,"T=",T,"N=",N,"Z=",Z,"CNT=",count(string))

	if(T==0 and N==0):
		return 0
	elif(count(string)>0):
		return count(string)/(N+T)
	else:
		return T/(Z*(T+N))	

def Pwb1(string):
	if(count(string)>0):
		return count(string)/(len(uni_count)*len(uni_list))
	else:
		print(string+": ZERO")
		return 0

def lam(context):
	vect = context.split()
	n = len(vect)
	t1 = 0
	t2 = 0
	if(n==2):
		for w in uni_count:
			if(context+" "+w in tri_count):
				t1+=1
				t2+=tri_count[context+" "+w]
	elif(n==1):
		for w in uni_count:
			if(context+" "+w in bi_count):
				t1+=1
				t2+=bi_count[context+" "+w]
	else: 	# n==0
		t1 = len(uni_count)
		t2 = len(uni_list)

	if(t1==0 and t2==0):
		return 0
	else:
		return t2/(t1+t2)

def Pfwb3(string):
	vect = string.split()
	word = vect[2]
	context = vect[0] + " " + vect[1]
	L = lam(context)
	# print(L,Pwb3(string),1-L,Pfwb2(vect[1]+" "+vect[2]))
	return L*Pwb3(string) + (1-L)*Pfwb2(vect[1]+" "+vect[2])

def Pfwb2(string):
	vect = string.split()
	word = vect[1]
	context = vect[0]
	L = lam(context)
	print(L,Pwb2(string),1-L,Pwb1(vect[1]))
	return L*Pwb2(string) + (1-L)*Pwb1(vect[1])

def WB_final(string,gram):	# string is sentence 
	string_list = string.split()
	prod = 1

	if(gram==3):
		for i in range(len(string_list)-2):
			aux_prob = Pfwb3(string_list[i]+" "+string_list[i+1]+" "+string_list[i+2])	# window size = 3
			prod*=aux_prob

	elif(gram==2):
		for i in range(len(string_list)-1):
			aux_prob = Pfwb2(string_list[i]+" "+string_list[i+1])	# window size = 2
			prod*=aux_prob

	elif(gram==1):
		for i in range(len(string_list)):
			aux_prob = Pwb1(string_list[i])	# window size = 1
			prod*=aux_prob
	
	return prod

def run():
	sent = input("input sentence:")
	sent = re.sub('[^A-Za-z]+', ' ', sent)
	sent = sent.lower()

	print(WB_final(sent,gram))
