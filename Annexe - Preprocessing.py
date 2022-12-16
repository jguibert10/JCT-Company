#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 13:57:06 2022

@author: charlesrollet
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, RobustScaler,MinMaxScaler
from xgboost import XGBRegressor
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV

df_temp = pd.read_excel('/Users/charlesrollet/Desktop/ENSAE 1A/Code PdP/df_traitee_test copie.xls')

column = ["date_mutation","valeur_fonciere", "type_local","surface_reelle_bati", "nombre_pieces_principales","longitude", "latitude"]
df = df_temp[column]

# On recode en binaire la variable type de bien
encoder = LabelEncoder()
df["type_local"]=encoder.fit_transform(df["type_local"])

# On regroupe les biens de plus de 9 pièces afin d'éviter le bruit que ces varibales pourraient engendrer
conditions = [df['nombre_pieces_principales']<9, df['nombre_pieces_principales']>=9]
values = [df['nombre_pieces_principales'].values, 'more_than_9']
df['test_nb_pieces'] = np.select(conditions, values)

# On convertit la date en datetime et on sépare les mois et les années
df["date_mutation"]=pd.to_datetime(df["date_mutation"]) 
df['année'] = df['date_mutation'].dt.year
df['mois'] = df['date_mutation'].dt.month
df.sort_values('date_mutation', ignore_index=True)

# regroupe les mois en demi semestre
conditions = [df['mois']<4, (df['mois']>=4) & (df['mois']<7), (df['mois']>=7) & (df['mois']<10),df['mois']>=10]
choiceliste = ['semestre_1','semestre_2','semestre_3','semestre_4']
df['semestre'] = np.select(conditions, choiceliste)

# On standardise les variables catégorielles mois et nombre de pièces
df_test = pd.get_dummies(df, columns = ['semestre'])
df_final = pd.get_dummies(df_test, columns = ['test_nb_pieces'])

# Création du DataFrame final`
df_new =pd.DataFrame(df_final)
new_list = ['date_mutation','nombre_pieces_principales','mois']
df_new=df_new.drop(new_list,axis=1)

# On standardise les variables continues
liste_annexe = ['surface_reelle_bati', 'latitude', 'longitude']
df_continu = df_new[liste_annexe]
sc = StandardScaler()
scale = sc.fit_transform(df_continu)
df_scale = pd.DataFrame(scale, columns = liste_annexe)

# On termine de construire notre base finale
for col in liste_annexe:
    df_new[col] = df_scale[col]

# On crée les bases features et cibles
Y = df_new["valeur_fonciere"]
X = df_new.drop("valeur_fonciere", axis=1)
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=11)

# On va choisir le meilleur standardiseur
sc = StandardScaler()
rs = RobustScaler()
minmax = MinMaxScaler()

X_train_st = sc.fit_transform(X_train)
X_test_st = sc.transform(X_test)

X_train_rob = rs.fit_transform(X_train)
X_test_rob = rs.transform(X_test)

X_train_mm = minmax.fit_transform(X_train)
X_test_mm = minmax.transform(X_test)

# On crée une fonction pour voir quel est le meilleur standardisateur
def meilleur_standardiseur(model_name):
    '''
    Find the best scaler regarding the model used with the accuracy score obtained
    Input: model_name, sklearn model
    '''
    better_score = 0
    better_scaler = ''

    X_train_list = [X_train_st, X_train_rob, X_train_mm]
    X_test_list = [X_test_st, X_test_rob, X_test_mm]
    scalers = ["Standard", "Robust", "MinMax"]
    
    for i in range(len(X_test_list)):
        model = model_name
        model.fit(X_train_list[i], Y_train)
        score = accuracy_score(Y_test, model.predict(X_test_list[i]))
        if score > better_score:
            better_score = score
            better_scaler = scalers[i]
        elif score == better_score:
            better_scaler += " / " + scalers[i]
    print("For {}, better score {} with {}.".format(model_name, better_score, better_scaler))

# On applique la fonction à 6 modèles différents 
meilleur_standardiseur(RandomForestClassifier()))
meilleur_standardiseur(DecisionTreeClassifier()))
meilleur_standardiseur(LogisticRegression()))
meilleur_standardiseur(KNeighborsClassifier()))
meilleur_standardiseur(SVC()))
meilleur_standardiseur(XGBRegressor()))
