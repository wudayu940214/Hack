from __future__ import division
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import re
from numpy import ones, array
from numpy.lib.scimath import log
import numpy as np
from django.shortcuts import render
import os
import json
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from operator import itemgetter
from collections import OrderedDict
import base64

stopwords = set(STOPWORDS)
module_dir = os.path.dirname(__file__)  # get current dir

def load_dataset():

	pos=open(os.path.join(module_dir, "positivewords.txt"), 'r')
	neg=open(os.path.join(module_dir, "negativewords.txt"), 'r')

	sent_list = []
	class_vec = []
	listP = []
	listN = []
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
			listP.append([strP])
		if len(strN) > 0:
			sent_list.append([strN])
			listN.append([strN])
	print(sent_list)
	print(class_vec)
	pos.close()
	neg.close()
	return sent_list, class_vec, listP, listN
 
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
		return 0
	else:
		return -1
def responseLoad(request):
	# data = json.loads(request.raw_post_data)
	print("**************" + request.POST.get('method'))

	if request.POST.get('method') == 'sa':
		total_result = sentiment_analysis()
		return JsonResponse(total_result, safe = False)
	else:
		return show_wordcloud()
	
def sentiment_analysis():
	list_sents, list_classes, listP, listN = load_dataset()
	my_vocab_list = create_vocab_list(list_sents)
#print(list_sents)
#print(my_vocab_list)
	train_mat = []
	for sent_in_doc in list_sents:
		train_mat.append(set_of_words2vec(my_vocab_list, sent_in_doc))
	p0V, p1V, pAb = trainNB(train_mat, list_classes)
	test_entry1 = ['It', 'is', 'better']
	#test_entry2 = ['abort', 'me']
	#test_context = set([])
	result =classifyNB(np.array(set_of_words2vec(my_vocab_list, test_entry1)), p0V, p1V, pAb)
	# number of each kind of word
	print(result)
	positiveCount = 0
	negativeCount = 0
	neutralCount = 0
	if result == 1:
		positiveCount += 1
	elif result == 0:
		negativeCount += 1
	else:
		neutralCount += 1
	if positiveCount > negativeCount:
		analysisResult = "positive"
	elif negativeCount > positiveCount:
		analysisResult = "negative"
	else:
		analysisResult = "netural"
	
	total_result = {
		"result": analysisResult,
		"positive": {
			"total": 50,
			"words": ["word1", "word3", "word3", "others"],
			"counts": [10, 10, 10, 10]
		},
		"negative": {
			"total": 40,
			"words": ["word1", "word3", "word4", "others"],
			"counts": [10, 10, 10, 10]
		},
		"netural": {
			"total": 10
		}
	}
	json_result = json.dumps(total_result)
	# print("**********" + type(total_result))
	return json_result
	#print(classifyNB(np.array(set_of_words2vec(my_vocab_list, test_entry2)), p0V, p1V, pAb))


def show_wordcloud():
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=200,
        max_font_size=40, 
        scale=3,
        random_state=1 # chosen at random by flipping a coin; it was heads
    ).generate(str("data matt"))

    fig = plt.figure()
    plt.axis('off')
    plt.imshow(wordcloud, interpolation="bilinear")
    wordcloud.to_file(os.path.join(module_dir, "rtrwa.jpeg"))
    f = open(os.path.join(module_dir, "rtrwa.jpeg"), 'rb')
    base64_data = base64.b64encode(f.read())
    return HttpResponse(base64_data, content_type='image/jpeg')


def index(request):
	return render(request, 'network.html')
