from __future__ import division
from django.http import HttpResponse
from django.shortcuts import render_to_response
import re
from numpy import ones, array
from numpy.lib.scimath import log
import numpy as np
from django.shortcuts import render
 
 
def load_dataset():
	pos=open("positivewords.txt", 'r', encoding="ISO-8859-1")
	neg=open("negativewords.txt", 'r', encoding="ISO-8859-1")
	sent_list = []
	class_vec = []
	for i in range(20):
		class_vec.append(i%2)
	for i in range(10):
		strP=pos.readline()
		strN=neg.readline()
		regP=re.compile('\\W*')
		regN=re.compile('\\W*')
		#listP = regP.split(strP.strip())
		#listN = regN.split(strN.strip())
		strP = strP.strip()
		strN = strN.strip()
		if len(strP) > 0:
			sent_list.append([strP])
		if len(strN) > 0:
			sent_list.append([strN])
	print(sent_list)
	print(class_vec)
	return sent_list, class_vec
 
def create_vocab_list(dataset):
	vocab_set = set([])
	for doc in dataset:
		vocab_set = vocab_set | set(doc)
	print(vocab_set)
	return list(vocab_set)
 
def set_of_words2vec(vocab_list, input_set):
	return_vec = [0] * len(vocab_list)
	
	for word in input_set:
		if word in vocab_list:
			return_vec[vocab_list.index(word)] = 1
	print(return_vec)
	return return_vec
 
def trainNB(train_matrix, train_catagory):
	num_train_docs = len(train_matrix)
	print(num_train_docs)
	print(len(train_catagory))
	num_words = len(train_matrix[0])
	pos_num = 0
	for i in train_catagory:
		if i == 1:
			pos_num += 1
	pAbusive = pos_num / float(num_train_docs)
	p0_num = np.ones(num_words)
	p1_num = np.ones(num_words)
	p0_demon = 2.0
	p1_demon = 2.0
	
	for i in range(num_train_docs):
		if train_catagory[i] == 1:
			p1_num += train_matrix[i]
			p1_demon += sum(train_matrix[i])
		else:
			p0_num += train_matrix[i]
			p0_demon += sum(train_matrix[i])
	
	p1_vect = np.log(p1_num / p1_demon)
	p0_vect = np.log(p0_num / p0_demon)
	
	return p0_vect, p1_vect, pAbusive
 
def classifyNB(vec2classify, p0_vec, p1_vec, pClass1):
	p1 = sum(vec2classify * p1_vec) + np.log(pClass1)
	p0 = sum(vec2classify * p0_vec) + np.log(1.0 - pClass1)
	
	if p1 > p0:
		return 1
	elif p0 > p1:
		return -1
	else:
		return 0
def responseLoad(request):
	list_sents, list_classes = load_dataset()
	my_vocab_list = create_vocab_list(list_sents)
#print(list_sents)
#print(my_vocab_list)
	train_mat = []
	for sent_in_doc in list_sents:
		train_mat.append(set_of_words2vec(my_vocab_list, sent_in_doc))
	p0V, p1V, pAb = trainNB(train_mat, list_classes)
	test_entry1 = ['It', 'is', 'better']
	test_entry2 = ['abort', 'me']
	test_context = set([])
	with open('twitter.json') as json_file:
		for line in json_file:
			data = json.loads(line)
		# remove link and specific character
			reg=re.compile('\\W*')
			context = reg.split(data["_source"]["title"])
			print(context)
			print(data["_source"]["title"])
	print(classifyNB(np.array(set_of_words2vec(my_vocab_list, test_entry1)), p0V, p1V, pAb))
	print(classifyNB(np.array(set_of_words2vec(my_vocab_list, test_entry2)), p0V, p1V, pAb))
def index(request):
	return render(request, 'network.html')