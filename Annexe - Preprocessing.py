#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 13:57:06 2022

@author: charlesrollet
"""

import numpy as np
import pandas as pd 
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelBinarizer 
from sklearn import linear_model
from sklearn.model_selection import train_test_split



df_temp = pd.read_excel('/Users/charlesrollet/Desktop/ENSAE 1A/Code PdP/df_traitee_test1.xls')

column = ["valeur_fonciere","type_local", "surface_reelle_bati", "nombre_pieces_principales","longitude", "latitude"]
df = df_temp[column]

scaler = StandardScaler()
New_long = scaler.fit_transform(df)

df_nor = pd.DataFrame(New_long ,columns = column)

Y = df_nor["valeur_fonciere"]
X = df_nor.drop("valeur_fonciere", axis=1)

X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=11)

reg = linear_model.LinearRegression()
reg_opt =reg.fit(X_train, Y_train)
print(1-reg_opt.score(X_test,Y_test))