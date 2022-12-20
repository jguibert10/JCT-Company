#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 20:29:05 2022

@author: charlesrollet
"""

# Import librairies
import numpy as np
import pandas as pd

# Models
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression, LinearRegression

# Model Selection and metrics
from sklearn.model_selection import cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.pipeline import make_pipeline
from statistics import mean
#import shap  

X_train = pd.read_excel('/Users/charlesrollet/Desktop/X_train_rob.xls')
X_test = pd.read_excel('/Users/charlesrollet/Desktop/X_test_rob.xls')
Y_train =  pd.read_excel('/Users/charlesrollet/Desktop/Y_train.xls')


# On définit de dictionnaires concernant les hyperparamètres de chaque modèle selectionné
dico_param_lr = {'linearregression__solver': ['gini', 'entropy'],
         'decisiontreeclassifier__splitter': ['best', 'random']}
dico_param_tree = {'decisiontreeclassifier__criterion': ['gini', 'entropy'],
         'decisiontreeclassifier__splitter': ['best', 'random']}
dico_param_rf = {"randomforestclassifier__n_estimators": np.arange(10, 100, 20),
              "randomforestclassifier__criterion": ['gini', 'entropy'],
              "randomforestclassifier__max_features": ['auto', 'sqrt', 'log2'],
              "randomforestclassifier__class_weight": [None, 'balanced']}
dico_param_log = {'logisticregression__solver': ['newton-cg', 'lbfgs', 
                                                 'liblinear', 'sag', 'saga']}
dico_param_knn = {"kneighborsclassifier__n_neighbors":np.arange(2, 10, 1),
                 "kneighborsclassifier__weights": ['uniform', "distance"],
                 "kneighborsclassifier__algorithm": ["auto", "ball_tree", "kd_tree", "brute"]}
dico_param_svm = {'svc__kernel':["linear", "poly", "rbf", "sigmoid"], 
           "svc__gamma":['scale', "auto"],
                 "svc__probability":[True, False]}

model_lr = make_pipeline(LinearRegression())
model_rf = make_pipeline(RandomForestClassifier())
model_tree = make_pipeline(DecisionTreeClassifier())
model_log = make_pipeline(LogisticRegression())
model_knn = make_pipeline(KNeighborsClassifier())
model_svm = make_pipeline(SVC())

# On souhaite que le recall et la precision soient les scores qui comptent le plus
SCORING = 'f1_weighted' 

# On crée une fonction qui donne les meilleurs hyperparamètres de chaque modèle
def best_param(X, Y, pipeline, dico_param):
    
    # On crée un grid search pour obtenir les meilleurs hyperparamètres
    grid = GridSearchCV(
        pipeline, 
        param_grid=dico_param,  
        cv=5, 
        refit=True,
        scoring=SCORING)
    
    grid.fit(X, Y)
    print(f"Le meilleur estimateur a {SCORING}={round(grid.best_score_, 2)}")
    
    # On garde le meilleur modèle en mémoire 
    best_model = grid.best_estimator_
    print("Le meilleur modèle est :", best_model[0])
    return best_model[0]

# On teste les meilleurs hyperparamètres pour les modèles sélectionnés
best_model_log = best_param(X_train, Y_train, model_log, dico_param_log)
best_model_tree = best_param(X_train, Y_train, model_tree, dico_param_tree)
best_model_knn = best_param(X_train, Y_train, model_knn, dico_param_knn)
best_model_svm = best_param(X_train, Y_train, model_svm, dico_param_svm)
best_model_rf = best_param(X_train, Y_train, model_rf, dico_param_rf)

# On crée une fonction pour tester le meilleur modèle et obtenir différents résultats sur ses performances 
def fit(X_train, X_test, Y_train, model):
    
    accuracy = mean(cross_val_score(model, X_train, Y_train, cv=(), scoring='accuracy'))
    auc = mean(cross_val_score(model, X_train, Y_train, cv=StratifiedKFold(), scoring='roc_auc'))
    precision = mean(cross_val_score(model, X_train, Y_train, cv=StratifiedKFold(), scoring='precision'))
    recall = mean(cross_val_score(model, X_train, Y_train, cv=StratifiedKFold(), scoring='recall'))
    f1_weighted = mean(cross_val_score(model, X_train, Y_train, cv=StratifiedKFold(), scoring='f1_weighted'))
    proba = model.predict_proba(X_test)[:,1]
    
    print('Accuracy: {:.3g}'.format(accuracy))
    print('Precision: {:.3g}'.format(precision))
    print('Recall: {:.3g}'.format(recall))
    print('F1 weighted: {:.3g}'.format(f1_weighted))
    print('AUC score: {:.3g}'.format(auc))
    
    return accuracy, auc, precision, f1_weighted, proba, recall

# On obtient différents scores pour le modèle qui obtient la meilleur précision suite à best_paraù
accuracy_log, auc_log, precision_log, f1_weighted_log, proba_log, recall_log = fit(X_train, X_test, Y_train, best_model_log)

