from __future__ import division
import re
from numpy import ones, array
from numpy.lib.scimath import log
from nltk import *
 
def loadDataSet():
    pos=open("demo.txt",'r')
    neg=open("demo.txt",'r')
    lst_all=[]
    classVec=[]
    for i in range(700):
        classVec.append(i%2)
    for i in range(350):
        str0=pos.readline()
        str1=neg.readline()
        regEx0=re.compile('\\W*')
        regEx1=re.compile('\\W*')
        lst_pos=regEx0.split(str0)
        lst_neg=regEx1.split(str1)
        lst_all.append([tok.lower() for tok in lst_pos if len(tok)>0])
        lst_all.append([tok.lower() for tok in lst_neg if len(tok)>0])
    return lst_all,classVec
 
def loadTestSet():
    pos=open("demo.txt",'r')
    neg=open("demo.txt",'r')
    lst_pos_test=[]
    lst_neg_test=[]
    for i in range(350):
        str0=pos.readline()
        regEx0=re.compile('\\W*')
        lst_pos=regEx0.split(str0)
        lst_pos_test.append([tok.lower() for tok in lst_pos if len(tok)>0])
    for i in range(350):
        str1=neg.readline()
        regEx1=re.compile('\\W*')
        lst_neg=regEx1.split(str1)
        lst_neg_test.append([tok.lower() for tok in lst_neg if len(tok)>0])
    # print 'loadtestset'
    return lst_pos_test,lst_neg_test
 
def createVocabList(dataSet):
    vocabSet = set([])  #create empty set
    for document in dataSet:
        vocabSet = vocabSet | set(document) #union of the two sets
    # print "createVocabList"
    return list(vocabSet)
 
def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
        # else:
            # print "the word: %s is not in my Vocabulary!" % word
    # print "bagbagbag"
    return returnVec
 
def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pCi = sum(trainCategory)/float(numTrainDocs)
    p0Num = ones(numWords); p1Num = ones(numWords)      #change to ones()
    p0Denom = 2.0; p1Denom = 2.0                        #change to 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num/p1Denom)          #change to log()
    p0Vect = log(p0Num/p0Denom)          #change to log()
    #print "training"
    return p0Vect,p1Vect,pCi
 
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)    #element-wise mult
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    # print "classifying"
    if p1 > p0:
        return 1
    else:
        return 0
 
def testingNB(lst_pos,lst_neg):
    listOPosts,listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat=[]
    pos_corre=[]
    neg_corre=[]
    for postinDoc in listOPosts:
        trainMat.append(bagOfWords2VecMN(myVocabList, postinDoc))
    p0V,p1V,pAb = trainNB0(array(trainMat),array(listClasses))
    for i in range(350):
        testEntry=lst_pos[i]
        thisDoc = array(bagOfWords2VecMN(myVocabList, testEntry))
        a=classifyNB(thisDoc,p0V,p1V,pAb)
        pos_corre.append(a)
    print("the positive text classify accuracy: {} ".format(1-sum(pos_corre)/350))
    print(sum(pos_corre))
    for i in range(350):
        testEntry = lst_neg[i]
        thisDoc = array(bagOfWords2VecMN(myVocabList, testEntry))
        a=classifyNB(thisDoc,p0V,p1V,pAb)
        neg_corre.append(a)
    print("the negative text classify accuracy: {} ".format(sum(neg_corre)/350))
    print(sum(neg_corre))
    print(p0V)
    print(p1V)
    print(pAb)
 
if __name__=='__main__':
    lst_pos,lst_neg=loadTestSet()
    testingNB(lst_pos,lst_neg)