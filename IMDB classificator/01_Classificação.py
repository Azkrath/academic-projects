# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 00:33:40 2017

@author: Azkrath
"""

import os
import re
import sys
import numpy as np
import CleanTextLib as ctl
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk import PorterStemmer 
from nltk import SnowballStemmer 
from nltk import LancasterStemmer
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.svm import LinearSVC

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
def plot_matrix(matrix, text):
    fig = plt.figure()
    plt.title("Matriz de Classificacao: " + text)
    plt.xticks(np.arange(0,8,1),("1", "2", "3", "4", "7", "8", "9", "10",""))  
    plt.yticks(np.arange(0,8,1),("1", "2", "3", "4", "7", "8", "9", "10","")) 
    plt.xlabel("Valores Estimados")
    plt.ylabel("Valores Verdadeiros")
    im = plt.imshow(matrix, cmap='rainbow', interpolation="none")
    fig.colorbar(im)
    plt.show()
    
# #############################################################################      
def plot_cmatrix(matrix, text):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.title("Matriz de Confusao: " + text)
    plt.xticks(np.arange(0,4,1),("P", "N", "", "", ""))  
    plt.yticks(np.arange(0,4,1),("P", "N", "", "", "")) 
    plt.xlabel("Valores Estimados")
    plt.ylabel("Valores Verdadeiros")
    im = plt.imshow(matrix, cmap='gray', interpolation="none")
    for y in range(matrix.shape[0]):
        for x in range(matrix.shape[1]):
            ax.text(x, y, '%.0f' % matrix[y, x], color='red', ha='center', va='center')
    fig.colorbar(im)
    plt.show()
    
# #############################################################################        
def print_matrix(matrix):
    print("Matriz de Confusão:")
    with fullprint():
        print(matrix)

# #############################################################################        
def stemmed_words(text_train):
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
trainScores = map(int,([name[name.find('_')+1:-4] for name in fnTrain]))
testScores = map(int, ([name[name.find('_')+1:-4] for name in fnTest]))

## Implementação do Bag of Words e implementação do método td-idf
## Obter palavras com minimo de frequencia de 5 ou mais documentos : min_df=5
## Aplicação de Stop Words para eliminação de palavras frequentes na lingua inglesa : stop_words="english"
## Aplicar tokenização para extração de palavras com 4 ou mais caracteres : tp  = r'\b\w\w\w\w+\b'
## Reduzir o vocabulário através de unigramas / bigramas : ngram_range=(1,2) 
## Aplicar stemming através de um analyzer : analyzer=stemmed_words
## Definir um vocabulário especifico: vocabulary=corpus
tp = r'\b\w\w\w\w+\b'
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

mindf = [5]
maxdf = [0.5]
for mi in mindf:
    for ma in maxdf:
        tfidf = TfidfVectorizer(min_df=mi, max_df=ma, token_pattern=tp, ngram_range=(1,2),
                                use_idf=True, sublinear_tf=True, analyzer=stemmed_words)
        tfidf = tfidf.fit(text_train)
        vocab = tfidf.get_feature_names()
        print("Tamanho vocab. = " + str(len(vocab)))
        print("Utilizando um min_df = " + str(mi) + " e um max_df = " + str(ma))
        print("-----------------------------------------------------------")
        # ----------------------------------------------------------
        ## Obter a representação na matriz esparsa
        Xtrain = tfidf.transform(text_train)
        Xtest = tfidf.transform(text_test)

        # #############################################################################
        # SVM classification model - LinearSVC,  Problema Binário
        ## Aplicação de um discriminante logistico com regularização
        ## l1 - Regularização Lasso
        ## l2 - Regularização Ridge
        print "A efetuar classificação binária com LinearSVM..."
        #param = [0.001, 0.01, 0.1, 0.5, 1, 5, 10, 30] 
        param = [0.1] ## Utilizar melhor parametro!!
        for i in param:
            print "Com Regularização = " + str(i)
            clf = LinearSVC(C = i, random_state=0, class_weight='balanced', max_iter=5000)
            clf = clf.fit(Xtrain, y_train)
            Pred = clf.predict(Xtest)
            ## Validar os acertos utilizando o discriminante logistico
            print('Acertos %.2f'%(clf.score(Xtrain,y_train)*100))
            print('Acertos %.2f'%(clf.score(Xtest,y_test)*100))
            # The mean squared error
            print("Mean squared error: %.2f" % mean_squared_error(y_test, Pred))
            # Explained variance score: 1 is perfect prediction
            print('Variance score: %.2f' % r2_score(y_test, Pred))
            matrix =  confusion_matrix(y_test, Pred)    ## Confusion Matrix
            print_matrix(matrix)
        #    plot_cmatrix(matrix,'LinearSVM');
            print classification_report(y_test, Pred, target_names=map(str,np.unique(y_test)))
        
        # #############################################################################
        ## Logistic Regression - Modelo Linear, Problema Binário
        ## Aplicação de um discriminante logistico com regularização
        ## l1 - Regularização Lasso
        ## l2 - Regularização Ridge
        print("A efetuar classificação binária com Regressão Logistica")
        #param = [0.001, 0.01, 0.1, 0.5, 1, 5, 10, 30] 
        param = [1] ## Utilizar melhor parametro!!
        for i in param:
            print "Com Regularização = " + str(i)
            logreg = LogisticRegression(penalty='l2',C=i,max_iter=5000)
            logreg.fit(Xtrain,y_train)
            Pred1 = logreg.predict(Xtest)
            predicted = logreg.predict_proba(Xtest)*100
            ## Validar os acertos utilizando o discriminante logistico
            print('Acertos %.2f'%(logreg.score(Xtrain,y_train)*100))
            print('Acertos %.2f'%(logreg.score(Xtest,y_test)*100))
            # The mean squared error
            print("Mean squared error: %.2f" % mean_squared_error(y_test, Pred1))
            # Explained variance score: 1 is perfect prediction
            print('Variance score: %.2f' % r2_score(y_test, Pred1))
            matrix2 =  confusion_matrix(y_test, Pred1)
            print_matrix(matrix2)
        #    plot_cmatrix(matrix2,'Log. Regression');
            print classification_report(y_test, Pred1, target_names=map(str,np.unique(y_test)))
        
        # #############################################################################
        # SVM classification model - LinearSVC,  Problema Multi-classe
        ## Aplicação de um discriminante logistico com regularização
        ## l1 - Regularização Lasso
        ## l2 - Regularização Ridge
        print "A efetuar classificação multiclasse com LinearSVM..."
        #param = [0.001, 0.01, 0.1, 0.5, 1, 5, 10, 30] 
        param = [0.1] ## Utilizar melhor parametro!!
        for i in param:
            print "Com Regularização = " + str(i)
            clf2 = LinearSVC(C=i, random_state=0, max_iter=5000)
            clf2 = clf2.fit(Xtrain, trainScores)
            Pred2 = clf2.predict(Xtest)
            ## Validar os acertos utilizando o discriminante logistico
            print('Acertos %.2f'%(clf2.score(Xtrain,trainScores)*100))
            print('Acertos %.2f'%(clf2.score(Xtest,testScores)*100))
            # The mean squared error
            print("Mean squared error: %.2f" % mean_squared_error(testScores, Pred2))
            # Explained variance score: 1 is perfect prediction
            print('Variance score: %.2f' % r2_score(testScores, Pred2))
            matrix3 =  confusion_matrix(testScores, Pred2)    ## Confusion Matrix
            print_matrix(matrix3)
        #    plot_matrix(matrix3,'LinearSVM');
            print classification_report(testScores, Pred2, target_names=map(str,np.unique(testScores)))
        
        # #############################################################################
        ## Logistic Regression - Modelo Linear, Problema Multi-classe
        ## Aplicação de um discriminante logistico com regularização
        ## l1 - Regularização Lasso
        ## l2 - Regularização Ridge
        print("A efetuar classificação multiclasse com Regressão Logistica")
        #param = [0.001, 0.01, 0.1, 0.5, 1, 5, 10, 30] 
        param = [1] ## Utilizar melhor parametro!!
        for i in param:
            print "Com Regularização = " + str(i)
            logreg2 = LogisticRegression(penalty='l2',C=i,max_iter=5000,
                                  multi_class='multinomial', solver='newton-cg')
            logreg2.fit(Xtrain,trainScores)
            Pred3 = logreg2.predict(Xtest)
            predicted = logreg2.predict_proba(Xtest)*100
            ## Validar os acertos utilizando o discriminante logistico
            print('Acertos %.2f'%(logreg2.score(Xtrain,trainScores)*100))
            print('Acertos %.2f'%(logreg2.score(Xtest,testScores)*100))
            # The mean squared error
            print("Mean squared error: %.2f" % mean_squared_error(testScores, Pred3))
            # Explained variance score: 1 is perfect prediction
            print('Variance score: %.2f' % r2_score(testScores, Pred3))
            matrix4 =  confusion_matrix(testScores, Pred3)
            print_matrix(matrix4)
        #    plot_matrix(matrix4,'Log. Regression');
            print classification_report(testScores, Pred3, target_names=map(str,np.unique(testScores)))

# #############################################################################
## Devolver o stdout
sys.stdout = orig_stdout
f.close()
print "Programa terminado!"