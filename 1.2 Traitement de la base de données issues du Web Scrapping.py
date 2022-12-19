#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 13:01:45 2022

@author: charlesrollet
"""

import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim 
import geopandas
from shapely.geometry import Point

# On lit la base issue du web scraping en renommant de la même manière les colonnes que celles issues de la base du gouv
df = pd.read_csv("Insérer la base issue du Web Scraping",\
                 names=['adresse_du_bien', 'valeur_fonciere','type_local', 'prix_m2', 'details'],\
                  index_col=0)
indexNames = df[ df['adresse_du_bien'] == 'addresse'].index
df.drop(indexNames , inplace=True)

# On supprime les doublons possibles issus du web scraping
df.drop_duplicates(keep = 'first', inplace=True)

# On crée une fonction afin de créer des colonnes à partir des anciennes
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

# On s'occupe d'abord de nettoyer les colonnes valeur_fonciere et prix_m2 en supprimant les chaînes de caractères 
df['prix_m2']=df['prix_m2'].str.split('€/m²').str[0]
df['prix_m2']=df['prix_m2'].str.replace(' ', '')
df['valeur_fonciere']=df['valeur_fonciere'].str.split('€').str[0] 
df['valeur_fonciere']=df['valeur_fonciere'].str.replace(' ', '')

# On crée deux colonnes à partir de adresse_du_bien qui contient l'adresse brute et la ville
df[['adresse', 'ville']]=df.adresse_du_bien.str.split(' - ', expand=True)

# On supprime toutes les données qui ne sont pas localisées à Paris issues du cadrillage rectangulaire du web scraping
indexNames = df[df['ville'] != 'PARIS'].index
df.drop(indexNames , inplace=True)

# On nettoye la colonne details pour contruire les colonnes nombre_pieces_principales, surface_reelle_bati et date_mutation
df[['nombre_pieces_principales','poubelle']] = df.details.apply(maxi_separator('Surface', 1))
df[['surface_reelle_bati','poubelle']] = df.poubelle.apply(maxi_separator('m²', 1))
df[['poubelle','date_mutation']] = df.poubelle.apply(maxi_separator('le', 1))
df[['poubelle','nombre_pieces_principales']] = df.nombre_pieces_principales.apply(maxi_separator('Pièces', 1))
df[['date_mutation','poubelle']] = df.date_mutation.apply(maxi_separator('+', 1))
df.drop(['poubelle', 'details'], axis=1, inplace=True)
liste_col = ['nombre_pieces_principales', 'surface_reelle_bati', 'date_mutation']
for col in liste_col:
    df[col]=df[col].str.split(',').str[1]
for col in liste_col:
    df[col]=df[col].str.split("'").str[1]

# On convertit les chaines de caratères numériques en nombres entiers
list_newcolumn = ['valeur_fonciere','prix_m2','nombre_pieces_principales','surface_reelle_bati']
for column in list_newcolumn:
    df[column]=df[column].astype(int)
    
# On supprime les données qui semblent de mauvaises qualités par rapport à leur prix au m2
indexNames = df[(df['prix_m2']< 9000)].index
df.drop(indexNames , inplace=True)
indexNames1 = df[(df['prix_m2']> 13000)].index
df.drop(indexNames1 , inplace=True)

# On convertit les adresses des biens en données géographiques
geolocator = Nominatim(timeout=5, user_agent = "myGeolocator")
df['coordinates'] = df['adresse_du_bien'].apply(geolocator.geocode)
df = df.dropna() #enlève les lignes avec des 'Nan'
df.reset_index(drop=True) #censer renuméroter le DataFrame mais ça marche pas mdrr
df['longitude'] = df['coordinates'].apply(lambda x: x.point.longitude)
df['latitude'] = df['coordinates'].apply(lambda x: x.point.latitude)

# On supprime les colonnes qui ne sont plus utiles et réordonne celles utiles afin que la base soit similaire à celle du gouv nettoyée 
df.drop(['coordinates', 'adresse_du_bien', 'adresse', 'ville', 'prix_m2'], axis=1, inplace=True)
df = df[['date_mutation','valeur_fonciere','type_local','surface_reelle_bati','nombre_pieces_principales','longitude','latitude']]

df.to_csv('Clean_WS.csv')
