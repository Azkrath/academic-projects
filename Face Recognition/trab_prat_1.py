# -*- coding: utf-8 -*-
"""
Created on Wed Nov 08 20:27:40 2017

@author: Azkrath
"""

import pickle as pk
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import PCA
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
from sklearn.metrics import precision_recall_curve

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
def plot_gallery(title, image, n_col=3, n_row=2):
    image_shape = (93, 70)
    plt.figure(figsize=(2. * n_col, 2.26 * n_row))
    plt.suptitle(title, size=16)
    plt.subplot(n_row, n_col, 2)
    plt.imshow(image.reshape(image_shape), 
                   cmap=plt.cm.gray,
                   interpolation='nearest')
    plt.xticks(())
    plt.yticks(())
    plt.subplots_adjust(0.01, 0.05, 0.99, 0.93, 0.04, 0.)
    
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
def plot_pca_components(X,Y):
    x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
    y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
    plt.figure(figsize=(8, 6))
    # Plot the training points
    plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=plt.cm.Set1,
                edgecolor='k')
    plt.xlabel('First Principal Component')
    plt.ylabel('Second Principal Component')
    plt.xticks(np.arange(0,1410,100))  
    plt.yticks(np.arange(0,1410,100)) 
    plt.grid()
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())

# #############################################################################
def plot_pca_comp_3d(Xr_data, X_target):
    # To getter a better understanding of interaction of the dimensions
    # plot the first three PCA dimensions
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.scatter(Xr_data[:,0], Xr_data[:,1], Xr_data[:,2], 
               c=X_target, marker='o')
    ax.set_title("First three PCA directions")
    ax.set_xlabel("1st eigenvector")
    ax.w_xaxis.set_ticklabels([])
    ax.set_ylabel("2nd eigenvector")
    ax.w_yaxis.set_ticklabels([])
    ax.set_zlabel("3rd eigenvector")
    ax.w_zaxis.set_ticklabels([])
    plt.show()
            
# #############################################################################
# n - Numero de vizinhos a testar
# a - numpy array que vai conter os scores
# X_train - Conjunto de faces de treino
# X_test - Conjunto de faces de teste
# Y_train - Conjunto de classes das faces de treino
# Y_test - Conjunto de classes das faces de teste
def calculate_knn(n, a, X_train, X_test, Y_train, Y_test):
    knn = KNeighborsClassifier(n_neighbors=n, weights='uniform')
    knn.fit(X_train, Y_train) 
    pred = knn.predict(X_test) 
    p = (np.round(knn.score(X_test, Y_test)*1000))/10.
    a.append(p)
    matrix =  confusion_matrix(Y_test,pred)    ## Confusion Matrix
    print_matrix(matrix)
    #plot_matrix(matrix,n);
    print "\n(Normal) Probabilidade de acertos (",n,"vizinhos)", p,"% (accuracy: ", accuracy_score(Y_test, pred),")"
    print classification_report(Y_test, pred, target_names=target_names)
    return knn, p
    
# #############################################################################
# n - Numero de vizinhos a testar
# a - numpy array que vai conter os scores
# splits - Numero de folds a efetuar
# x_data - Conjunto de faces 
# x_target - Conjunto de classes
def calculate_knn_kfold(n, a, splits, x_data, x_target):
    knn = KNeighborsClassifier(n_neighbors=n, weights='uniform')
    kfolds = StratifiedKFold(n_splits=splits)
    scores = cross_val_score(knn,x_data,x_target,cv=kfolds)
    results = cross_val_predict(knn, x_data, x_target, cv=kfolds)
    p = (np.round(np.mean(scores)*1000))/10.
    a.append(p)
    matrix =  confusion_matrix(x_target, results)    ## Confusion Matrix
    print_matrix(matrix)
    #plot_matrix(matrix,n);
    print "\n(kFold) Probabilidade de acertos (",n,"vizinhos)",p,"%"
    print classification_report(x_target, results, target_names=target_names)
    return knn, p
    
# #############################################################################
# X_data - Conjuntos de dados
# n_components - Numero de componentes a testar
def calculate_pca_manual(X_data, X_target, n):
    Cx = np.cov(X_data)
    (v,W) = np.linalg.eig(Cx)
    v = v.real
    idx = np.argsort(-v)
    v = v[idx]
    W = W[:,idx]
    W = W[:,v>=1e-10]
    W = W.real

    # Normalizar os valores proprios
    v=v/np.sum(v)
    
    # Soma cumulativa
    #L = np.cumsum(v)
    
    # Obter num. componentes que contêm n de variância
    #k = np.sum(L<=n)
    
    #print "Numero de componentes que contêm " + str(n*100) + "% da variância: " + str(k)

    #W = W[:,0:k]
    W = W[:,0:n]
           
    ## Remover a média dos dados
    mx = np.mean(X_data,axis=1)
    mx = mx[:,np.newaxis]
    Xm_train = X_data - mx
    
    ## Projetar as faces nas n components principais
    Y = np.dot(W.T,Xm_train)
    #Y = np.dot(W.T,X)
    
    ## Normalizar a variância de cada dimensão
    Yn = np.dot(np.diag(np.std(Y,axis=1)**-1),Y)

    ## Efetuar reconstrução dos dados
    Xr = np.dot(W, Yn)
    Xr_data = Xr #+  mx
    
    #plot_gallery("Bush without PCA", X_data[0])
    #plot_gallery("Bush with PCA", Xr_data[0])
    
    return Xr_data, k
    
# #############################################################################
# X_train - Conjunto de faces de treino
# X_test - Conjunto de faces de teste
# n_components - Numero de componentes a testar
def calculate_pca(X_train, X_test, n_components):        
    pca = PCA() 
    pca = PCA(n_components=n_components, svd_solver='randomized', whiten=True)
    pca.fit(X_train)
    x_data_pca = pca.transform(X_train)
#    X_test_pca = pca.transform(X_test)
    print("\nX_train_pca.shape: {}".format(x_data_pca.shape))
#    print("X_test_pca.shape: {}".format(X_test_pca.shape))
    #Y = pca.inverse_transform(x_data_pca[0])
    #plot_gallery("Bush", x_data[0])
    #plot_gallery("Bush", Y)
    return x_data_pca #, X_test_pca
    
# #############################################################################
# n - Numero de vizinhos a testar
# a - numpy array que vai conter os scores
# x_data - Conjunto de faces 
# x_target - Conjunto de classes
def calculate_kfold_pca(knn, x_data, x_target, kfold, n_components, max_perc, max_comp):
    pca = PCA()
    pca = PCA(n_components)
    pca.fit(x_data)
    x_data_pca = pca.transform(x_data)
    scores = cross_val_score(knn, x_data_pca, x_target, cv=kfold) ## Percentage of score with knn with optimal neighbours
    if max_perc < ((np.round(np.mean(scores)*1000))/10.):
        max_perc = ((np.round(np.mean(scores)*1000))/10.)
        max_comp = n
    print "Probabilidade de acertos (",n_components,"componentes)", (np.round(np.mean(scores)*1000))/10.,"%"
    b.append((np.round(np.mean(scores)*1000))/10.)
    return x_data_pca, max_perc, max_comp
    
# #############################################################################
# x_data - Conjunto de faces 
# x_target - Conjunto de classes
def calculate_svc(x_data, x_target, values):
    param_grid = [{'kernel': ['rbf'], 'C': [0.001, 0.01, 0.1, 1, 10, 100], 'gamma': [0.001, 0.01, 0.1, 1, 10, 100]}] 
    #param_grid = [{'kernel': ['linear'],'C': [0.001, 0.01, 0.1, 1, 10, 100]}]
    print "A efetuar classificação com SVC..."
    clf = GridSearchCV(SVC(kernel='rbf', class_weight='balanced'), param_grid, cv=5)
    X_train, X_test, Y_train, Y_test = train_test_split(x_data, x_target, random_state=0)
    clf.fit(X_train,Y_train)
    Pred = clf.predict(X_test)
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
    matrix =  confusion_matrix(Y_test, Pred)    ## Confusion Matrix
    print_matrix(matrix)
    plot_matrix(matrix,n);
    print classification_report(Y_test, Pred, target_names=values)
    
    #clf = SVC(kernel='rbf', random_state=0, gamma=0.01, C=10, class_weight='balanced')
    #kfolds = StratifiedKFold(n_splits=5)
    #scores = cross_val_score(clf,x_data,x_target,cv=kfolds) # precision
    #results = cross_val_predict(clf, x_data, x_target, cv=kfolds)
    #print(classification_report(x_target, results, target_names=values))
    #matrix = confusion_matrix(x_target, results)
    #print_matrix(matrix)
    
# #############################################################################
def plot_figure_knn(neighbours, a):
    plt.figure()
    plt.plot(neighbours, a, 'ro')
    plt.plot(neighbours, a, 'k--')
    plt.title("Representacao da taxa de acertos face ao numero de vizinhos")
    plt.xticks(np.arange(0,neighbours[len(neighbours)-1],10))  #intervalos no x = 1
    plt.yticks(np.arange(0,50,5) ) #intervalos no y = 1/4
    plt.xlabel("Numero de vizinhos")
    plt.ylabel("Taxa em % de acertos")
    plt.grid()
    plt.savefig('graficokNN.png')

# #############################################################################
def plot_figure_pca(n_components, d):
    plt.figure()
    plt.plot(n_components, d, 'ro')
    plt.plot(n_components, d, 'k--')
    plt.title("Representacao da taxa de acertos face ao numero de componentes")
    plt.xticks(np.arange(0,600,100))  
    plt.yticks(np.arange(35,39,1)) 
    plt.grid()
    plt.xlabel("Numero de components")
    plt.ylabel("Taxa em % de acertos")
    plt.savefig('graficokNN_PCA.png')
    
# #############################################################################
def plot_matrix(matrix, n_components):
    plt.figure()
    plt.title("Matriz de Classificacao com " + str(n_components) +" vizinho(s)")
    plt.xlabel("Valores Estimados")
    plt.ylabel("Valores Verdadeiros")
    plt.imshow(matrix, cmap='gray', interpolation="none")
    plt.savefig("graficokNN_PCA_" + str(n_components) + ".png")

def plot_cmatrix(matrix):
    plt.figure()
    plt.title("Matriz de Confusao")
    plt.xticks(np.arange(0,4,1),("", "TN", "", "TN", ""))  
    plt.yticks(np.arange(0,4,1),("", "FP", "", "FN", "")) 
    plt.xlabel("Valores Estimados")
    plt.ylabel("Valores Verdadeiros")
    plt.imshow(matrix, cmap='gray', interpolation="none")
    
def print_matrix(matrix):
    print("Matriz de Confusão:")
    with fullprint():
        print(matrix)
        
def plot_roc_curve(X_test, Y_score):
    fpr, tpr, thresholds = roc_curve(Y_test, Y_score)
    plt.plot(fpr, tpr, label="ROC Curve")
    plt.xlabel("FPR")
    plt.ylabel("TPR (recall)")
    # find threshold closest to zero
    close_zero = np.argmin(np.abs(thresholds))
    plt.plot(fpr[close_zero], tpr[close_zero], 'o', markersize=10,
    label="threshold zero", fillstyle="none", c='k', mew=2)
    plt.legend(loc=4)

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

print("Total dataset size:")
print("n_samples: %d" % x_target.shape[0])
print("n_features: %d" % n_features)
print("n_classes: %d" % n_classes)

# #############################################################################
# kNN 
# e.g.: neighbours = np.array([1,5,8,13,20,30,50,100])
# Criar uma lista de numeros para a análise KNN
myList = list(range(6,8))

# obter apenas os numeros ímpares
neighbours = filter(lambda x: x % 2 != 0, myList)
a=[]
a2 = []
# #############################################################################
# Separar os dados em um conjunto de treino e um conjunto de teste
# X_train, X_test, Y_train, Y_test = train_test_split(x_data, x_target, test_size=0.25, random_state=42) # Stratified kFold
X_train, X_test, Y_train, Y_test = train_test_split(x_data, x_target, stratify=x_target, random_state=0)

# Normal    
print "Efetuar classificação das imagens com classificador KNN:"
p = 0
best_p = 0
best_n = 0
for n in neighbours:
    knn, p = calculate_knn(n, a, X_train, X_test, Y_train, Y_test)
    if p > best_p:
        best_p = p
        best_knn = knn
        best_n = n

plot_figure_knn(neighbours, a)

print "\nNumero de vizinhos optimos: ", best_n, " vizinho(s)."

# #############################################################################
#kFold
print "Efetuar classificação das imagens com classificador KNN utilizando validação cruzada:"

p2 = 0
best_p2 = 0
best_n2 = 0
splits = 10
for n in neighbours:
    knn2, p2 = calculate_knn_kfold(n, a2, splits, x_data, x_target)
    if p2 > best_p2:
        best_p2 = p2
        best_knn2 = knn2
        best_n2 = n
        
plot_figure_knn(neighbours, a2)

print "\nNumero de vizinhos optimos com validação cruzada: ", best_n2, " vizinho(s)."
        
# #############################################################################
# Compute a PCA (eigenfaces) on the face dataset (treated as unlabeled
# dataset): unsupervised feature extraction / dimensionality reduction

#n_components = np.array([50,100,150,200,500,750,1000,1400])
n_components = np.array([50])
#n_var = np.array([0.99, 0.98, 0.95, 0.92, 0.90])
#n_var = np.array([0.95])
b = []
c = []
d = []
k_var = []

print "\nEfetuar o processamento das faces utilizando PCA e estimar o numero optimo de componentes principais:" 
max_comp = 0
max_perc = 0
best_p = 0
k = 0
X_train, X_test, Y_train, Y_test = train_test_split(x_data, x_target, stratify=x_target, random_state=0)
for n in n_components:
    print "Utilizando " + str(n) + " componentes:"
    #train_pca, test_pca = calculate_pca(X_train, X_test, n)
    plot_pca_comp_3d(x_data, x_target)
    #train_pca = calculate_pca(x_data, x_target, n)    
    train_pca, k = calculate_pca_manual(x_data, x_target, n)
    plot_pca_comp_3d(train_pca, x_target)
    #k_var.append(k)
    #knn3, p3 = calculate_knn(best_n, d, train_pca, test_pca, Y_train, Y_test)
    knn3, p3 = calculate_knn_kfold(best_n2 , d, splits, train_pca, x_target)
    print "Probabilidade de acertos (",n,"componentes)", p3,"%"
    if p3 > max_perc:
        max_perc = p3
        max_comp = n
        x_data_pca = train_pca
        #x_test_pca = test_pca
    
plot_figure_pca(n_components, d)
print "\nO Numero optimo de componentes prinicpais é: ",max_comp," Componentes."

#print "\nEfetuar o processamento das faces utilizando PCA manual com " + str(max_comp) + " componentes principais:" 
#npc = max_comp
#Xr_data = calculate_pca_manual(x_data, npc)
#X_train, X_test, Y_train, Y_test = train_test_split(Xr_data, x_target, stratify=x_target, random_state=0)
#calculate_knn(best_n, b, X_train, X_test, Y_train, Y_test)
#calculate_knn_kfold(best_n2, c, splits, Xr_data, x_target)

# #############################################################################
# SVM classification model - SVC
print("Efetuar o processamento das faces com outro classificador sobre os dados processados:")
print("A utilizar um classificador SVM")
#calculate_svc(Xr_data, x_target)
calculate_svc(x_data_pca, x_target, target_names)

# #############################################################################
# Problema de classificação binário

classOne  = x_data[:,x_target == 8]
classTwo  = x_data[:,x_target != 8]

x2_target = np.copy(x_target)
x2_target[x_target==8] = 1
x2_target[x_target!=8] = 0

print("Faces que são o Bush: " + str(classOne.shape[1]))
print("Faces que não são o Bush: " + str(classTwo.shape[1]))

m1 = np.mean(classOne,axis=1)
m2 = np.mean(classTwo,axis=1)

m1 = m1[:,np.newaxis]
m2 = m2[:,np.newaxis]

X1 = x_data - m1
X2 = x_data - m2

D1=np.sqrt(np.sum(X1*X1,axis=1))
D2=np.sqrt(np.sum(X2*X2,axis=1))

Dtotal = np.vstack((D1,D2))

eClass=np.argmin(Dtotal,axis=0)

TP = float(np.sum(eClass[x2_target==1]==1)) # (TP)
FN = float(np.sum(eClass[x2_target==1]==0)) # (FN)
FP = float(np.sum(eClass[x2_target==0]==1)) # (FP)
TN = float(np.sum(eClass[x2_target==0]==0)) # (TN)

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

print_matrix(CM)
plot_cmatrix(CM)

report_values = ["Not G.W. Bush", "G.W. Bush"]
print classification_report(x2_target, eClass, target_names=report_values)

# #############################################################################
plot_pca_comp_3d(x_data, x2_target)
x_data_pca = calculate_pca(x_data, x2_target, 50)    
#train_pca, k = calculate_pca_manual(x_data, x_target, n)
plot_pca_comp_3d(x_data_pca, x2_target)

print("A utilizar um classificador SVM com classificação binária")
calculate_svc(x_data_pca, x2_target, report_values)