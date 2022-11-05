# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 19:12:07 2022

@author: julien
"""
    
import numpy as np
import pandas as pd 
from sklearn import linear_model

#Récupération de la base de données
df = pd.read_excel('df_traitee_test.xls')
print(df.shape)

def estimateur(arr, typ, surf, nbp):
    global df #récupération de la variable globale
    df2 = df #création d'une variable locale
    #Filtrage
    df2 = df2.loc[(df2["code_postal"] == arr) & 
                (df2["type_local"].str.contains("Appartement")) &
                (abs(df2['surface_reelle_bati']-surf) <= 20) &
                (abs(df2['nombre_pieces_principales']-nbp <= 1))]
    if len(df2) == 0:
        return None
    
    #Vraisemblance enlever les valeurs extrêmes (5% au dessus et en dessous)
    df2.sort_values(by=['valeur_fonciere'], inplace=True)
    df2.reset_index(drop=True, inplace=True)
    
    n = df2.shape[0]
    k_5 = np.floor(0.05*n) #partie entière
    index_minmax = np.arange(k_5, dtype=int).tolist() + ((n-1)-np.arange(k_5, dtype=int)).tolist()
    df2.drop(index=index_minmax, inplace=True)

    #Regression
    Y = df2["valeur_fonciere"].values.tolist()
    x_1 = np.array(
        df2["surface_reelle_bati"].values.tolist()
        ) #régresseur surface
    x_0 = np.ones(x_1.shape[0], dtype=int) #la constante de régression
    X = np.c_[x_0, x_1].tolist() #créer une matrice n ligne 2 colonne
    #print(X[:10]) #10 premières lignes
    reg = linear_model.LinearRegression()
    reg.fit(X, Y)
    return reg.predict([(1, surf)])[0]

