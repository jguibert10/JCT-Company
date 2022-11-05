#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 08:45:57 2022

@author: charlesrollet
"""

import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim 
import geopandas
from shapely.geometry import Point


df = pd.read_csv("/Users/charlesrollet/Desktop/Cadrillage.csv",\
                 names=['numéro_du_bien', 'adresse_du_bien', 'prix_du_bien', 'date_de_vente_du_bien', 'détails_du_bien'],\
                  index_col=0)
indexNames = df[ df['adresse_du_bien'] == 'addresse'].index
df.drop(indexNames , inplace=True)
#df.drop(index =2235, inplace=True)
df.drop_duplicates(keep = 'first', inplace=True)

# Reconfiguration des données brutes du Dataframe

def func(x):
    if x[0]=='s':
        a=x[1:]
        return str(a)
    else:
         return x

def separator(c):
    return lambda x: pd.Series(str(x).split(c))

def maxi_separator(c, d):
    return lambda x: pd.Series(str(x).split(c, d))


list_column = df.columns.tolist()


#Création des nouvelles colonnes pertinentes
df['adresse globale'] = \
    df['adresse_du_bien'].str.replace('\n', ' ')
df[['adresse precise','arrondissement']] = \
    df.adresse_du_bien.apply(separator('\n'))
df[['prix de vente','prix du m2']] = \
    df.prix_du_bien.apply(separator('\n')) 
df[['date de vente','colonne']] = \
    df.date_de_vente_du_bien.apply(separator('\n')) 
df[['type de bien','details_bis']] = \
    df.détails_du_bien.apply(maxi_separator(' ',1)) 
df[['nombre de pièces','surface_du_bien']] = \
    df.details_bis.apply(separator('pièce')) 
df[['surface du bien en m2','poubelle']] = \
    df.surface_du_bien.apply(maxi_separator('m', 1))
#Suppression des anciennes colonnes et des doublons
df.drop(list_column, axis=1, inplace=True)
df.drop(['colonne', 'surface_du_bien', 'poubelle', 'details_bis'], axis=1, inplace=True)
df.drop_duplicates()
    
#Nettoyage des données pour pouvoir les manipuler
df['date de vente']=df['date de vente'].str[9:]
df['arrondissement']=df['arrondissement'].str.split(' PARIS').str[0]
df['prix du m2']=df['prix du m2'].str.split('€/m²').str[0] 
df['prix de vente']=df['prix de vente'].str.split('€').str[0] 
df['prix de vente']=df['prix de vente'].str.replace(' ', '')
df['prix du m2']=df['prix du m2'].str.replace(' ', '')
df['surface du bien en m2']= df['surface du bien en m2'].apply(func)
#encodage binaire pour type de bien
df['type de bien']=df['type de bien'].str.replace('Appartement','0')
df['type de bien']=df['type de bien'].str.replace('Maison','1')
#Convertion des variables quantitatives en entiers
list_newcolumn = list(df)
list_newcolumn.remove('date de vente')
list_newcolumn.remove('adresse precise')
list_newcolumn.remove('adresse globale')
for column in list_newcolumn:
    df[column]=df[column].astype(int)
print(df)

n = len(df.index)

#geolocator = Nominatim(timeout=5, user_agent = "myGeolocator")
#df['coordinates'] = df['adresse globale'].apply(geolocator.geocode)
#df = df.dropna() #enlève les lignes avec des 'Nan'
#df.reset_index(drop=True) #censer renuméroter le DataFrame mais ça marche pas mdrr
#df['longitude'] = df['coordinates'].apply(lambda x: x.point.longitude)
#df['latitude'] = df['coordinates'].apply(lambda x: x.point.latitude)
#df.drop(['coordinates'], axis=1, inplace=True)
#print(df['longitude'], df['latitude'], n, len(df.index))


df.to_csv('Clean data.csv')



