from read_documents import ReadDocuments
from nltk.stem import PorterStemmer
import math,re,sys,getopt
from operator import itemgetter
from collections import OrderedDict

file = open('demo.txt', 'r')
book = file.read()
stoplist = set()
stoplistFile = None
stemmer = PorterStemmer()

def addStopList():
    with open('stop_list.txt', 'r') as f:
        for line in f:
            line = line.strip().split()
            for x in line:
                stoplist.add(stemmer.stem(x.lower()))

def tokenize():
    if book is not None:
        words = book.lower().split()
        return words
    else:
        return None
def count_word(tokens):
    count = 0
    words = dict()
    for element in tokens:
        # Remove Punctuation
        element = stemmer.stem(element)
        if element in stoplist:
            continue
        word = element.replace(",","")
        word = word.replace(".","")
        if word not in words:
            words[word] = 1
        else:
            words[word] += 1
    sorted_word = sorted(words.items(), key=itemgetter(1), reverse=True)
    print(sorted_word)

words = tokenize()
addStopList()
count_word(words)