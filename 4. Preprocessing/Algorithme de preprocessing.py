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
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression, BayesianRidge
from sklearn.model_selection import cross_val_score

df_temp = pd.read_excel('/Users/charlesrollet/Desktop/df_traitee_final.xls')

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

# On crée les bases features et cibles
Y = pd.DataFrame(df_new["valeur_fonciere"])
X = df_new.drop("valeur_fonciere", axis=1)
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=11)

# On chosisit de réindexer les dataframe afin d'éviter que la réinsersion des colonnes de new_list standardisée pose pb
X_train = X_train.reset_index(drop = True)
X_test = X_test.reset_index(drop = True)
Y_train = Y_train.reset_index(drop = True)
Y_test = Y_test.reset_index(drop = True)

# On retire du dataframe X_train les variables continues pour les standardiser
liste_annexe = ['surface_reelle_bati', 'latitude', 'longitude']
df_continu = X_train[liste_annexe]
df_continu_test = X_test[liste_annexe]

# On utilise 3 principaux Standardisateurs
sc = StandardScaler()
rs = RobustScaler()
minmax = MinMaxScaler()

# On standardise les variables continues dans les bases train et test selon les 3 standardisateurs choisis
scale = sc.fit_transform(df_continu)
df_scale = pd.DataFrame(scale, columns = liste_annexe)
scale_test = sc.transform(df_continu_test)
df_scale_test = pd.DataFrame(scale_test, columns = liste_annexe)

robust = rs.fit_transform(df_continu)
df_robust = pd.DataFrame(robust, columns = liste_annexe)
robust_test = rs.transform(df_continu_test)
df_robust_test = pd.DataFrame(robust_test, columns = liste_annexe)

MinMax = minmax.fit_transform(df_continu)
df_MinMax = pd.DataFrame(MinMax, columns = liste_annexe)
MinMax_test = minmax.transform(df_continu_test)
df_MinMax_test = pd.DataFrame(MinMax_test, columns = liste_annexe)

# On termine de construire nos bases finales
X_train_st = X_train.copy()
X_train_rob = X_train.copy()
X_train_mm = X_train.copy()

X_test_st = X_test.copy()
X_test_rob = X_test.copy()
X_test_mm = X_test.copy()

for col in liste_annexe:
    X_train_st[col] = df_scale[col]
    X_test_st[col] = df_scale_test[col]
    
for col in liste_annexe:
    X_train_rob[col] = df_robust[col]
    X_test_rob[col] = df_robust_test[col]
    
for col in liste_annexe:
    X_train_mm[col] = df_MinMax[col]
    X_test_mm[col] = df_MinMax_test[col]
# On crée une fonction pour voir quel est le meilleur standardisateur
def meilleur_standardiseur(model_name):
    
    better_score = 0
    better_scaler = ''

    X_train_list = [X_train_st, X_train_rob, X_train_mm]
    X_test_list = [X_test_st, X_test_rob, X_test_mm]
    scalers = ["Standard", "Robust", "MinMax"]
    
    for i in range(len(X_test_list)):
        model = model_name
        model.fit(X_train_list[i], Y_train)
        score = model.score(X_test_list[i], Y_test)
        if score > better_score:
            better_score = score
            better_scaler = scalers[i]
        elif score == better_score:
            better_scaler += " / " + scalers[i]
    print("Pour le modèle {}, better score {} avec {}.".format(model_name, better_score, better_scaler))

# On applique la fonction à 6 modèles différents 
meilleur_standardiseur(LinearRegression()))
meilleur_standardiseur(RandomForestRegressor()))
meilleur_standardiseur(DecisionTreeRegressor()))
meilleur_standardiseur(LogisticRegression()))
meilleur_standardiseur(KNeighborsRegressor)))
meilleur_standardiseur(BayesianRidge()))

#df_new.to_excel('base finale pour le ML')
#df_new.to_csv('base finale pour le ML')
