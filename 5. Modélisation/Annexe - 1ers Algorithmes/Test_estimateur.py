# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 20:27:38 2022

@author: julien
"""

import numpy as np
import random
import pandas as pd 
from modelisation import estimateur

#Récupération de la base de données
df = pd.read_excel('df_traitee_test.xls')
print(df.shape)

#Création base train & base test
n = df.shape[0]
np.random.seed(10) #racine de l'aléatoire pour la reproductibilité
index_test = np.random.randint(n, size= np.floor(0.20*n).astype(int))
df_train = df.drop(index=index_test)
df_test = df.drop(df_train.index)
#ou utiliser df_test = df.sample(frac=0.20) mais non reproductible

#Création d'un estimateur référence celui du m_2
liste_prixm2 = [13490, 11910, 12700, 12170, 12610, 13950, 13080, 11730, 10800, 10160,\
                10320, 9720, 9210, 10070, 9950, 10950, 10320, 9670, 8900, 9170]
def estimateur_prixm2(arr, surf):
    temp = str(arr).replace('75', "")
    temp = int(temp)
    return liste_prixm2[temp-1]*surf

#Accuracy de l'estimateur
list_erreur = []
list_erreur_m2 =[]
for i in range(df_test.shape[0]):
    #variable de référence
    prix = df_test.iloc[i]["valeur_fonciere"]
    #variables testee
    arr = df_test.iloc[i]["code_postal"]
    typ = df_test.iloc[i]["type_local"]
    surf = df_test.iloc[i]["surface_reelle_bati"]
    nbp = df_test.iloc[i]["nombre_pieces_principales"]
    
    #estimations
    val_estimee = estimateur(arr, typ, surf, nbp)
    if val_estimee is None:
        continue
    erreur = abs(val_estimee - prix)/prix
    list_erreur.append(erreur)
    
    val_estimee_m2 = estimateur_prixm2(arr, surf)
    erreur_m2 = abs(val_estimee_m2 - prix)/prix
    list_erreur_m2.append(erreur_m2)

print(1-np.mean(np.array(list_erreur))) #0.818
print(1-np.mean(np.array(list_erreur_m2))) #0.819

    
    
