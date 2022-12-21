#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 20:29:05 2022

@author: charlesrollet
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression, LinearRegression


from sklearn.model_selection import cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error,mean_squared_log_error

X_train_st = pd.read_csv('X_train_st.cvs')
X_train_rob = pd.read_csv('X_train_rob.cvs')
X_train_mm = pd.read_csv('X_train_mm.cvs')
X_test_st = pd.read_csv('X_test_st.cvs')
X_test_rob = pd.read_csv('X_test_rob.cvs')
X_test_mm = pd.read_csv('X_test_mm.cvs')
Y_test = pd.read_csv('Y_test.cvs')
Y_train = pd.read_csv('Y_train.cvs')

# On définit de dictionnaires concernant les hyperparamètres de chaque modèle selectionné
dico_param_tree = {'decisiontreeregressor__criterion': ['squared_error #(ou 'mse' en fonction de votre version sklearn)#', 'friedman_mse', 'absolute_error', 'poisson'],
         'decisiontreeregressor__splitter': ['best', 'random']}
dico_param_rf = {"randomforestregressor__n_estimators": np.arange(10, 100, 20),
              "randomforestregressor__criterion": ['squared_error#(ou 'mse' en fonction de votre version sklearn)#', 'absolute_error', 'friedman_mse','poisson'],
              "randomforestregressor__max_features": ['auto', 'sqrt', 'log2']}
dico_param_log = {'logisticregression__solver': ['newton-cg', 'lbfgs', 
                                                 'liblinear', 'sag', 'saga']}
dico_param_knn = {"kneighborsregressor__n_neighbors":np.arange(2, 10, 1),
                 "kneighborsregressor__weights": ['uniform', "distance"],
                 "kneighborsregressor__algorithm": ["auto", "ball_tree", "kd_tree", "brute"]}
dico_param_svc = {'svc__kernel':["linear", "poly", "rbf", "sigmoid"], 
           "svc__gamma":['scale', "auto"],
                 "svc__probability":[True, False]}

model_lr = make_pipeline(LinearRegression())
model_rf = make_pipeline(RandomForestRegressor())
model_tree = make_pipeline(DecisionTreeRegressor())
model_log = make_pipeline(LogisticRegression())
model_knn = make_pipeline(KNeighborsRegressor())
model_svm = make_pipeline(SVC())

# On souhaite que le recall et la precision soient les scores qui comptent le plus
SCORING = 'r2' 

# On crée une fonction qui donne les meilleurs hyperparamètres de chaque modèle
def best_param(X, Y, pipeline, dico_param):
    
    # On crée un grid search pour obtenir les meilleurs hyperparamètres
    grid = GridSearchCV(
        pipeline, 
        param_grid=dico_param,  
        cv=3, 
        refit=True,
        scoring=SCORING)
    
    grid.fit(X, Y)
    print(f"Le meilleur estimateur a {SCORING}={round(grid.best_score_, 2)}")
    
    # On garde le meilleur modèle en mémoire 
    best_model = grid.best_estimator_
    print("Le meilleur modèle est :", best_model[0])
    return best_model[0]

# On teste les meilleurs hyperparamètres pour les modèles sélectionnés
best_model_lr = model_lr
best_model_log = best_param(X_train, Y_train, model_log, dico_param_log)
best_model_tree = best_param(X_train, Y_train, model_tree, dico_param_tree)
best_model_knn = best_param(X_train, Y_train, model_knn, dico_param_knn)
best_model_svm = best_param(X_train, Y_train, model_svm, dico_param_svm)
best_model_rf = best_param(X_train, Y_train, model_rf, dico_param_rf)

# On crée une fonction pour tester le meilleur modèle et obtenir différents résultats sur ses performances 
def fit(mettre_X_train, mettre_X_test, mettre_Y_train, model):
    
    mean_absolute_error = mean(cross_val_score(model, mettre_X_train, mettre_Y_train, cv=StratifiedKFold(), scoring='neg_mean_absolute_error'))
    mean_squared_error = mean(cross_val_score(model, mettre_X_train, mettre_Y_train, cv=StratifiedKFold(), scoring='neg_mean_squared_error'))
    max_error = mean(cross_val_score(model, mettre_X_train, mettre_Y_train, cv=StratifiedKFold(), scoring='max_error'))
    explained_variance =mean(cross_val_score(model, mettre_X_train, mettre_Y_train, cv=StratifiedKFold(), scoring='explained_variance'))
    mean_poisson_deviance = mean(cross_val_score(model, mettre_X_train, mettre_Y_train, cv=StratifiedKFold(), scoring='neg_mean_poisson_deviance'))

    print('mean_absolute_error: {:.3g}'.format(mean_absolute_error))
    print('mean_squared_error: {:.3g}'.format(mean_squared_error))
    print('max_error: {:.3g}'.format(max_error))
    print('explained_variance: {:.3g}'.format(explained_variance))
    print('mean_poisson_deviance: {:.3g}'.format(mean_poisson_deviance))
    
    return mean_absolute_error, mean_squared_error, max_error, explained_variance, mean_poisson_deviance

# On obtient différents scores pour le modèle qui obtient la meilleur précision suite à best_paraù
mean_absolute_error_log, mean_squared_error_log, max_error_log, explained_variance_log, mean_poisson_deviance_log = fit(X_train_st, X_test_st, Y_train, best_model_log)
mean_absolute_error_tree, mean_squared_error_tree, max_error_tree, explained_variance_tree, mean_poisson_deviance_tree = fit(X_train_mm, X_test_mm, Y_train, best_model_tree)
mean_absolute_error_knn, mean_squared_error_knn, max_error_knn, explained_variance_knn, mean_poisson_deviance_knn = fit(X_train_rob, X_test_rob, Y_train, best_model_knn)
mean_absolute_error_svm, mean_squared_error_svm, max_error_svm, explained_variance_svm, mean_poisson_deviance_svm = fit(X_train_st, X_test_st, Y_train, best_model_svm)
mean_absolute_error_rf, mean_squared_error_rf, max_error_rf, explained_variance_rf, mean_poisson_deviance_rf = fit(X_train_st, X_test_st, Y_train, best_model_rf)
mean_absolute_error_lr, mean_squared_error_lr, max_error_lr, explained_variance_lr, mean_poisson_deviance_lr = fit(X_train_st, X_test_st, Y_train, best_model_lr)

# On crée une fonction qui renvoie les meilleurs features 
def best_features(model, X_train, seuil) :     
    features_importances = []
    index_best_features = []
    list_results = model.feature_importances_.tolist()
    best_features = []
    for i in range(len(list_results)):
        if list_results[i] > seuil :
            index_best_features.append(i)
            features_importances.append(list_results[i])
            best_features.append(X_train.columns[i])
    return best_features, features_importances

# Pour le modèle RandomForest Regressor on regarde les features les plus importantes 
mean_absolute_error, mean_squared_error, max_error, explained_variance, mean_poisson_deviance = fit(X_train_st, X_test_st, Y_train, best_model_rf)

best_features_rf, features_importance_rf = best_features(best_model_rf, X_train_st, 0.01)

pd.DataFrame(features_importance_rf, index = best_features_rf).plot.bar(color='purple')
plt.suptitle('Feature importances pour RandomForest', fontsize=15)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.legend(fontsize=10)
plt.show()
