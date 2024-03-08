# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 22:54:06 2017

@author: Azkrath
"""

import os
import re
import sys
import numpy as np
import CleanTextLib as ctl
from sklearn import datasets
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk import PorterStemmer 
from nltk import SnowballStemmer 
from nltk import LancasterStemmer
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge

# #############################################################################
def getTrainData():
    Dtrain=datasets.load_files(os.getcwd() + "/aclImdb/train")
    return Dtrain

def getTestData():
    Dtest=datasets.load_files(os.getcwd() + "/aclImdb/test")
    return Dtest

# #############################################################################
class fullprint:
    'context manager for printing full numpy arrays'

    def __init__(self, **kwargs):
        if 'threshold' not in kwargs:
            kwargs['threshold'] = np.nan
        self.opt = kwargs

    def __enter__(self):
        self._opt = np.get_printoptions()
        np.set_printoptions(**self.opt)

    def __exit__(self, type, value, traceback):
        np.set_printoptions(**self._opt)
    
# #############################################################################
def print_matrix(matrix):
    print("Matriz de Confusão:")
    with fullprint():
        print(matrix)

# #############################################################################        
def stemmed_words(text_train):
    stemmer = LancasterStemmer()
    return (stemmer.stem(w) for w in analyzer(text_train))

# #############################################################################
## Redirecionar o stdout para ficheiro    
print "Programa iniciado!"
orig_stdout = sys.stdout
f = open('out.txt', 'w')
sys.stdout = f

# #############################################################################
## Obter os dados de treino e de teste
reviews_train = getTrainData()
reviews_test = getTestData()
text_train, y_train = reviews_train.data, reviews_train.target
text_test, y_test = reviews_test.data, reviews_test.target

## Limpeza dos dados de treino
## Limpeza pode ser efetuada aqui ou na biblioteca específica
text_train = [doc.replace('<br />',' ') for doc in text_train]
text_train = [re.sub('[\W_\d]+', ' ', doc.lower()) for doc in text_train]

## Limpeza dos dados de teste
## Limpeza pode ser efetuada aqui ou na biblioteca específica
text_test = [doc.replace('<br />',' ') for doc in text_test]
text_test = [re.sub('[\W_\d]+', ' ', doc.lower()) for doc in text_test]

## Obter os nomes dos ficheiros
fnTrain = reviews_train.filenames
fnTest = reviews_test.filenames 

## Obter as pontuações das criticas
## Obter as pontuações das criticas
trainScores = map(int,([name[name.find('_')+1:-4] for name in fnTrain]))
testScores = map(int, ([name[name.find('_')+1:-4] for name in fnTest]))

## Implementação do Bag of Words e implementação do método td-idf
## Obter palavras com minimo de frequencia de 5 ou mais documentos : min_df=5
## Discartar palavras que aparecem em mais de 80% dos documentos: max_df = 0.8
## Aplicação de Stop Words para eliminação de palavras frequentes na lingua inglesa : stop_words="english"
## Aplicar tokenização para extração de palavras com 4 ou mais caracteres : tp  = r'\b\w\w\w\w+\b'
## Reduzir o vocabulário através de unigramas / bigramas : ngram_range=(1,2) 
## Aplicar stemming através de um analyzer : analyzer=stemmed_words
## Definir um vocabulário especifico: vocabulary=corpus
tp  = r'\b\w\w\w+\b'
# ----------------------------------------------------------
## Construir um analyzer para efetuar o stemming
analyzer = TfidfVectorizer().build_analyzer()
## Escolher o tipo de stemming a aplicar
#stemmer = LancasterStemmer()
stemmer = SnowballStemmer('english')
#stemmer = PorterStemmer()
# ----------------------------------------------------------
## Alternativa - utilizar biblioteca de limpeza de texto
## Pior performance nos classificadores
#text_trainset = ''.join(text_train)
#corpus = ctl.create_dict(text_trainset, 5, 20, 5)
#tfidf = TfidfVectorizer(min_df=5, max_df=0.8, token_pattern=tp, vocabulary=corpus)
# ----------------------------------------------------------
#tfidf = TfidfVectorizer(min_df=10, max_df=0.5, token_pattern=tp, ngram_range=(2,2), 
#                        use_idf=True, sublinear_tf=True, analyzer=stemmed_words)
# ----------------------------------------------------------
mindf = [8]
maxdf = [0.8]
for mi in mindf:
    for ma in maxdf:
        tfidf = TfidfVectorizer(min_df=mi, max_df=ma, token_pattern=tp, use_idf=True, 
                                sublinear_tf=True, ngram_range=(1,2), analyzer=stemmed_words)
        # ----------------------------------------------------------
        tfidf = tfidf.fit(text_train)
        vocab = tfidf.get_feature_names()
        #print len(vocab)
        # ----------------------------------------------------------
        ## Obter a representação na matriz esparsa
        Xtrain = tfidf.transform(text_train)
        Xtest = tfidf.transform(text_test)
        
        # #############################################################################
        ## Linear Regression - Regressão, Problema Binário/Multiclasse
        ## Aplicação de um discriminante logistico com regularização
        ## l1 - Regularização Lasso
        ## l2 - Regularização Ridge
        print("A efetuar regressão com Regressão Linear")
        print("Tamanho vocab. = " + str(len(vocab)))
        print("-----------------------------------------------------------")
        # ----------------------------------------------------------
        ## Regressão Linear Simples
        #linreg = LinearRegression()
        #linreg = linreg.fit(Xtrain,y_train)
        # ----------------------------------------------------------
        ## Regressão linear usando Ridge
        #linreg = Ridge(alpha=1)
        #linreg = linreg.fit(Xtrain,trainScores)
        #pred2 = linreg.predict(Xtest)
        # ----------------------------------------------------------
        ## Regressão com Descida de Gradiente Estocástica
        #param = [0.00001, 0.0001, 0.001, 0.01, 0.1, 0.5, 1, 10] 
        #eta = [0.0001, 0.001, 0.01, 0.1, 1, 10]
        #power = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.0]
        param = [0.0001] ## Utilizar melhor parametro!!
        eta = [0.01] ## Utilizar melhor parametro!
        power = [0.1] ## Utilizar melhor parametro!
        for i in param:
            for j in eta:
                for k in power:
                    print "Com Regularização = " + str(i) + " e Tx. Aprend. = " + str(j) + " e Power_t = " + str(k)
                    linreg = SGDRegressor(alpha=i, loss="squared_loss", penalty="l1", 
                                          learning_rate='invscaling',  max_iter=5000, eta0=j, 
                                          tol=1e-3, power_t=k)
                    linreg = linreg.fit(Xtrain,trainScores)
                    pred = linreg.predict(Xtest)
                    print('coeficiente R2 (treino): %f' %(linreg.score(Xtrain,trainScores)))
                    print('coeficiente R2 (teste): %f' %(linreg.score(Xtest,testScores) ))
                    # The mean squared error
                    print("Mean squared error: %.2f" % mean_squared_error(testScores, pred))
                    # Explained variance score: 1 is perfect prediction
                    print('Variance score: %.2f' % r2_score(testScores, pred))
                    print("-----------------------------------------------------------")
        
        # #############################################################################     
        # Conversão em classificação binária
        y_pred = pred.copy()
        y_pred[pred >= 5] = 1
        y_pred[pred < 5] = 0
        TP = float(np.sum(y_pred[y_test==1]==1)) # (TP)
        FN = float(np.sum(y_pred[y_test==1]==0)) # (FN)
        FP = float(np.sum(y_pred[y_test==0]==1)) # (FP)
        TN = float(np.sum(y_pred[y_test==0]==0)) # (TN)
        p11 = float(TP/(TP+FN)) # (recall)
        p22 = float(TN/(FP+TN)) # (specificity)
        p12 = float(FN/(TP+FN))
        p21 = float(FP/(FP+TN))
        CM=np.array([[p11,p12],[p21,p22]])
        PPV = float(TP/(TP+FP)) # (precision)
        Fscore = float(2*((PPV*p11)/(PPV+p11)))
        PTE = float((FP+FN)/(TP+FP+TN+FN))
        PPP = float((TP+FN)/(TP+FN+FP+TN))
        PPN = float((FP+TN)/(TP+FN+FP+TN))
        NPV = float(TN/(TN+FN))
        FDR = float(FP/(TP+FP))
        FOR = float(FN/(TN+FN))
        matrix =  confusion_matrix(y_test, y_pred)    ## Confusion Matrix
        print_matrix(matrix)
        #    plot_cmatrix(matrix,'LinearSVM');
        print classification_report(y_test, y_pred, target_names=map(str,np.unique(y_test)))
# #############################################################################
## Devolver o stdout
sys.stdout = orig_stdout
f.close()
print "Programa terminado!"