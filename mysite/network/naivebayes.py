from __future__ import division
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
# from django.shortcuts import render_to_response
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
from elasticsearch import Elasticsearch
import time
from .elasticsearch_data import queryES

stopwords = set(STOPWORDS)
module_dir = os.path.dirname(__file__)  # get current dir


def load_dataset():

	pos=open(os.path.join(module_dir, "positivewords.txt"), 'r')
	neg=open(os.path.join(module_dir, "negativewords.txt"), 'r')

	sent_list = []
	class_vec = []
	listP = []
	listN = []
	for i in range(500):
		class_vec.append(i%2)
	for i in range(200):
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
	#print("**************" + request.POST.get('method'))

	if request.POST.get('method') == 'sa':
		Jsonresult = sentiment_analysis("the", "", "")
		return JsonResponse(Jsonresult, safe = False)
	else:
		return show_wordcloud()

# def queryText(keywords, name, period, index="twitter_data", doc_type="test_type", ip="148.70.167.220"):
#     es = Elasticsearch(ip)
#     if period == '':
#         period = "01/01/2014 12:00 AM - 04/18/2019 11:59 PM"
#     starttime_str = period.split(" - ")[0].replace("/", " ").strip()
#     endtime_str = period.split(" - ")[1].replace("/", " ").strip()
#     print("*" * 30)
#     starttime = time.strftime("%Y-%m-%dT%H:%M", time.strptime(starttime_str, "%m %d %Y %I:%M %p"))
#     endtime = time.strftime("%Y-%m-%dT%H:%M", time.strptime(endtime_str, "%m %d %Y %I:%M %p"))
#     # result = starttime + ";" + endtime
#     # starttime = result.split(';')[0]
#     # endtime = result.split(';')[1]
#     querywithname = {
#         "query": {
#             "bool": {
#                 "must": [
#                     {'match': {'text': keywords}},
#                     {'match': {'name': name}},
#                     {"range": {"time": {"gte": starttime, "lt": endtime}}},
#                 ]
#             }
#         }
#     }
#     querywithoutname = {
#         "query": {
#             "bool": {
#                 "must": [
#                     {'match': {'text': keywords}},
#                     {"range": {"time": {"gte": starttime, "lt": endtime}}},
#                 ]
#             }
#         }
#     }
#     query = querywithname
#     if name == '':
#         query = querywithoutname
#     allDoc = es.search(index=index, body=query)
#     list = allDoc['hits']['hits']
#     return list
    

def sentiment_analysis(keyword, name, period):
	list_sents, list_classes, listP, listN = load_dataset()
	my_vocab_list = create_vocab_list(list_sents)
#print(list_sents)
#print(my_vocab_list)
	train_mat = []
	analysisResult ="positive"
	for sent_in_doc in list_sents:
		train_mat.append(set_of_words2vec(my_vocab_list, sent_in_doc))
	p0V, p1V, pAb = trainNB(train_mat, list_classes)
	#test_entry1 = ['It', 'is', 'better']
	#test_entry2 = ['abort', 'me']
	#test_context = set([])
	textContentList = queryES(keyword, name, period)
	print("*" *30)
	print(keyword + " " + name + " " + period)
	print(str(textContentList))
	for line in textContentList:
		print("sdfdsfsdfsdfsf" + line)
		reg = re.compile('\\W*')
		solveData = reg.split(line['_source']['text'])
		print("wangbadanwangbadan"+solveData[0])
		result =classifyNB(np.array(set_of_words2vec(my_vocab_list, solveData)), p0V, p1V, pAb)
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
			print(listP)
			for word in listP:
				mydictP = dict()
				if word in solveData:
					mydictP[word] += 1
			#sorted_wordP = sorted(mydictP.items(), key=itemgetter(1), reverse=True)
			sorted_wordP = str(sorted(mydictP.items(), key=itemgetter(1), reverse=True))
			print("-----------------------------------"+sorted_wordP)
			sorted_wordP = re.sub(r'\[', "{", sorted_wordP)
			sorted_wordP = re.sub(r'\]', "}", sorted_wordP)
			sorted_wordP = re.sub(r'\'\,', "':", sorted_wordP)
			sorted_wordP = re.sub(r'\(|\)', "", sorted_wordP)
			
			indexP  = 1
			for keyP in sorted_wordP:
				if indexP == 1:
					wordP1 = keyP
					print(sorted_wordP[keyP])
					wordP1Value = int(sorted_wordP[keyP])
					indexP += 1
					continue
				elif indexP == 2:
					wordP2 = keyP
					wordP2Value = int(sorted_wordP[keyP])
					indexP += 1
					continue
				else:
					wordP3 = keyP
					wordP3Value = int(sorted_wordP[keyP])
			otherCountP = sum(sorted_wordP.values()) - sorted_wordP[wordP1] - sorted_wordP[wordP2] - sorted_wordP[wordP3]
		elif negativeCount > positiveCount:
			analysisResult = "negative"
			for word in listN:
				mydictN = dict()
				if word in solveData:
					mydictN[word] += 1
			#sorted_wordN = sorted(mydictN.items(), key=itemgetter(1), reverse=True)
			sorted_wordN = str(sorted(mydictN.items(), key=itemgetter(1), reverse=True))
			sorted_wordN = re.sub(r'\[', "{", sorted_wordN)
			sorted_wordN = re.sub(r'\]', "}", sorted_wordN)
			sorted_wordN = re.sub(r'\'\,', "':", sorted_wordN)
			sorted_wordN = re.sub(r'\(|\)', "", sorted_wordN)
			print(sorted_wordN)
			indexN = 1
			for keyN in range(3):
				if indexN == 1:
					wordN1 = keyN
					wordN1Value = int(sorted_wordN[keyN])
					indexN +=1
					continue
				elif indexN == 2:
					wordN2 = keyN
					wordN2Value = int(sorted_wordN[keyN])
					indexN +=1
					continue
				else:
					wordN3 = keyN
					wordN3Value = int(sorted_wordN[keyN])
			otherCountN = sum(sorted_wordP.values() - sorted_wordP[wordN1] - sorted_wordP[wordN2] - sorted_wordP[wordN3])
		else:
			analysisResult = "netural"
	# 	result =classifyNB(np.array(set_of_words2vec(my_vocab_list, test_entry1)), p0V, p1V, pAb)
	# # number of each kind of word
	# 	print(result)
	# 	positiveCount = 0
	# 	negativeCount = 0
	# 	neutralCount = 0
	# 	if result == 1:
	# 		positiveCount += 1
	# 	elif result == 0:
	# 		negativeCount += 1
	# 	else:
	# 		neutralCount += 1
	# 	if positiveCount > negativeCount:
	# 		analysisResult = "positive"
	# 		for word in listP:
	# 			mydictP = dict()
	# 			if word in test_entry1:
	# 				mydictP[word] += 1
	# 	#sorted_wordP = sorted(mydictP.items(), key=itemgetter(1), reverse=True)
	# 		sorted_wordP = str(sorted(mydictP.items(), key=itemgetter(1), reverse=True))
	# 		sorted_wordP = re.sub(r'\[', "{", sorted_wordP)
	# 		sorted_wordP = re.sub(r'\]', "}", sorted_wordP)
	# 		sorted_wordP = re.sub(r'\'\,', "':", sorted_wordP)
	# 		sorted_wordP = re.sub(r'\(|\)', "", sorted_wordP)
	# 		indexP  = 1
	# 		for keyP in sorted_wordP:
	# 			if count == 1:
	# 				wordP1 = keyP
	# 				wordP1Value = sorted_wordP[keyP]
	# 				indexP += 1
	# 				continue
	# 			elif count == 2:
	# 				wordP2 = keyP
	# 				wordP2Value = sorted_wordP[keyP]
	# 				indexP += 1
	# 				continue
	# 			else:
	# 				wordP3 = keyP
	# 				wordP3Value = sorted_wordP[keyP]
	# 				otherCountP = sum(sorted_wordP.values()) - sorted_wordP[wordP1] - sorted_wordP[wordP2] - sorted_wordP[wordP3]
	# 	elif negativeCount > positiveCount:
	# 		analysisResult = "negative"
	# 		for word in listN:
	# 			mydictN = dict()
	# 			if word in test_entry1:
	# 				mydictN[word] += 1
	# 	#sorted_wordN = sorted(mydictN.items(), key=itemgetter(1), reverse=True)
	# 		sorted_wordN = str(sorted(mydictN.items(), key=itemgetter(1), reverse=True))
	# 		sorted_wordN = re.sub(r'\[', "{", sorted_wordN)
	# 		sorted_wordN = re.sub(r'\]', "}", sorted_wordN)
	# 		sorted_wordN = re.sub(r'\'\,', "':", sorted_wordN)
	# 		sorted_wordN = re.sub(r'\(|\)', "", sorted_wordN)
	# 		indexN = 1
	# 		for keyN in range(3):
	# 			if i == 1:
	# 				wordN1 = keyN
	# 				wordN1Value = sorted_wordN[keyN]
	# 				indexN +=1
	# 				continue
	# 			elif i == 2:
	# 				wordN2 = keyN
	# 				wordN2Value = sorted_wordN[keyN]
	# 				indexN +=1
	# 				continue
	# 			else:
	# 				wordN3 = keyN
	# 				wordN3Value = sorted_wordN[keyN]
	# 				otherCountN = sum(sorted_wordP.values() - sorted_wordP[wordN1] - sorted_wordP[wordN2] - sorted_wordP[wordN3])
	# 	else:
	# 		analysisResult = "netural"
	total_result = {
		"result": analysisResult,
		"positive": {
			"total": positiveCount,
			"words": [wordP1, wordP2, wordP3, "others"],
			"counts": [int(wordP1Value), int(wordP2Value), int(wordP3Value), int(otherCountP)]
		},
		"negative": {
			"total": negativeCount,
			"words": [wordN1, wordN2, wordN3, "others"],
			"counts": [int(wordN1Value), int(wordN2Value), int(wordN3Value0), int(otherCountN)]
		},
		"netural": {
			"total": neutralCount
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
