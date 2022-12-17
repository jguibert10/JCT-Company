# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 17:32:56 2022

@author: julien
"""

import numpy as np
import pandas as pd

#Récupération de la base de données
df_temp = pd.read_csv(Insérer la base du gouvernement)
#df_temp = pd.read_excel(Insérer la base du gouvernement)
#mettre la base non traitée

#Sélection des variables d'intérêts
column = ["date_mutation", "nature_mutation", 
          "valeur_fonciere",#type int64
          "type_local", "surface_reelle_bati", "nombre_pieces_principales",
          "longitude", "latitude"]
df = df_temp[column]

#Filtrage des données
temp = df[df['nature_mutation'].str.contains('Vente') &
              df['type_local'].str.contains('Appartement|Maison')]

#Données manquantes
temp = temp.dropna()
temp = temp.reset_index(drop=True)
#print(temp.isnull().sum().sum()) #nombre de NaN dans le df

#Changement du type des données
list_column_int = ["nombre_pieces_principales", "code_postal", 
                   "surface_reelle_bati", "valeur_fonciere",
                   "adresse_numero"]
for column in list_column_int:
    temp[column]=temp[column].astype(int)

#Dernière modification pour enlever les ventes groupées d'appart
index_supp = []
compteur = 0
for i in range(1, temp.shape[0]):
    if temp.iloc[i]["valeur_fonciere"] != temp.iloc[i-1]["valeur_fonciere"]:
        compteur = 0
    else:
        if compteur == 0:
            index_supp.append(i-1)
            index_supp.append(i)
            compteur = 1
        else:
            index_supp.append(i)
temp.drop(index=index_supp, inplace=True)
temp = temp.reset_index(drop=True)

#Vraisemblance
temp_2 = temp[abs(temp["valeur_fonciere"]-10000*temp["surface_reelle_bati"])
              /temp["valeur_fonciere"] <= 1.5]

temp_2.drop(['nature_mutation'], axis=1, inplace=True)

#temp_2.to_csv(r'df_traitee_test.csv')
#temp_2.to_excel(r'df_traitee_test.xls')
