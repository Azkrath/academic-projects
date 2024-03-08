# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 18:28:46 2017

@author: Azkrath
"""
import pickle as pk
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
import pandas as pd

# #############################################################################
def plot_heatmap(data):
    x_value = np.array([0.001, 0.01, 0.1, 1, 10, 100])
    y_value = np.array([0.001, 0.01, 0.1, 1, 10, 100])
    plt.figure()
    plt.xticks(np.arange(6), x_value)
    plt.yticks(np.arange(6), y_value)
    heatmap = plt.pcolor(data)
    plt.xlabel('Gamma')
    plt.ylabel('Cost')
    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            plt.text(x + 0.5, y + 0.5, '%.4f' % data[y, x],
                     horizontalalignment='center',
                     verticalalignment='center',
                     )
    
    plt.colorbar(heatmap)
    
    plt.show()
    
# #############################################################################
# x_data - Conjunto de faces 
# x_target - Conjunto de classes
def calculate_svc(x_data, x_target):
    param_grid = [{'kernel': ['rbf'], 'C': [0.001, 0.01, 0.1, 1, 10, 100], 'gamma': [0.001, 0.01, 0.1, 1, 10, 100]}] 
    #param_grid = [{'kernel': ['linear'],'C': [0.001, 0.01, 0.1, 1, 10, 100]}]
    print "A efetuar classificação com SVC..."
    clf = GridSearchCV(SVC(kernel='rbf', class_weight='balanced'), param_grid, cv=5)
    X_train, X_test, Y_train, Y_test = train_test_split(x_data, x_target, random_state=0)
    clf.fit(X_train,Y_train)    
    print("Test set score: {:.2f}".format(clf.score(X_test, Y_test)))
    print("Best parameters: {}".format(clf.best_params_))
    print("Best cross-validation score: {:.2f}".format(clf.best_score_))
    print("Best estimator:\n{}".format(clf.best_estimator_))
    # convert to DataFrame
    results = pd.DataFrame(clf.cv_results_)
    # show the first 5 rows
    print(results.head())
    scores = np.array(results.mean_test_score).reshape((6,6))
    plot_heatmap(scores)   
    return scores    

# #############################################################################
# Carregar os dados a partir do ficheiro como numpy arrays
carasBD = pk.load(open('lfw_raw.p', 'rb'))

X = carasBD.data
n_features = X.shape[1]

# encontrar as shapes para o plotting
n_samples, h, w = carasBD.images.shape
y = carasBD.target
target_names = carasBD.target_names
n_classes = target_names.shape[0]

###############################################################################
# Obter apenas 50 imagens por pessoa para que os resultados não seja enviesados
mask = np.zeros(y.shape, dtype=np.bool)
for target in np.unique(y):
    mask[np.where(y == target)[0][:50]] = 1
    
x_data = X[mask]
x_target = y[mask]

# normalizar os valores de cinzento para ficar entre 0 e 1
x_data = x_data / 255.

# #############################################################################
# Problema de classificação binário

classOne  = x_data[:,x_target == 8]
classTwo  = x_data[:,x_target != 8]

print("Faces que são o Bush: " + str(classOne.shape[1]))
print("Faces que não são o Bush: " + str(classTwo.shape[1]))

m1 = np.mean(classOne,axis=1)
m2 = np.mean(classTwo,axis=1)

X1 = x_data - m1[:,np.newaxis]
X2 = x_data - m2[:,np.newaxis]

D1=np.sqrt(np.sum(X1*X1,axis=0))
D2=np.sqrt(np.sum(X2*X2,axis=0))

Dtotal = np.vstack((D1,D2))

eClass=np.argmin(Dtotal,axis=0)

TP = float(np.sum(eClass[x_target==8]==0)) # (TP)
FN = float(np.sum(eClass[x_target==8]==0)) # (FN)
FP = float(np.sum(eClass[x_target!=8]==1)) # (FP)
TN = float(np.sum(eClass[x_target!=8]==0)) # (TN)

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

print("Efetuar o processamento das faces com outro classificador sobre os dados processados:")
print("A utilizar um classificador SVM")
#calculate_svc(Xr_data, x_target)

x2_target = np.copy(x_target)
x2_target[x_target==8] = 0
x2_target[x_target!=8] = 1
svc_scores = calculate_svc(x_data, x2_target)

# #############################################################################