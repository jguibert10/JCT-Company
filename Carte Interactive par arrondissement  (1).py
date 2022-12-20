#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd 
import geopandas as gpd
import numpy as np
from folium.features import GeoJsonTooltip
from folium.features import GeoJsonPopup


# On  télécharge un fichier geojson issu du site du gouvernement représentant les arrondissements de Paris. On le transforme dans un premier temps en un DataFrame grâce à geopandas. 

# In[4]:


geojson = gpd.read_file('arrondissements.geojson')


# In[5]:


geojson.head()


# On récupère nos données immobilières  

# In[6]:


df = pd.read_csv("Clean_final.csv")
print(df.shape)


# In[7]:


df.head()


# On supprime les lignes du DataFrame qui n'ont pas la donnée code postal 

# In[8]:


df['arrondissement'] = df['arrondissement'].fillna(0)


# On supprime les lignes n'ayant pas de code postal. 
# 

# In[9]:


list = []
a = -1
for i in df['arrondissement']: 
    a = a+1
    try : 
        i = int(i)
    except ValueError : 
        list.append(a)
        
df2 = df.drop(df.index[list])

#On vérifie qu'il ne reste pas de code postal au format incorrect dans arrondissement 
list2 = []
a = -1
for i in df2['arrondissement']: 
    a = a + 1 
    try : 
        list2.append(int(i))
    except ValueError : 
        print(i)
    


df2['arrondissement'] = df2['arrondissement'].astype('int64')


# On récupère le numéro d'arrondissement à partir du code postal.

# In[10]:


Arrondissement_1 = []
for i in df2['arrondissement'] : 
    Arrondissement_1.append(i%1000)
    

df2['arrondissement'] = Arrondissement_1


# On crée un nouveau DataFrame qui résume par arrondissement les prix au mètre carré. 

# In[11]:


table = np.round(pd.pivot_table(df2, index = df2["arrondissement"], 
                       values = ["prix du m2"]))


df3 = table.reset_index()


# On fusionne le DataFrame avec le geojson avec pour clé l'arrondissement (arrondissement dans df3, c_ar dans geojson) 

# In[12]:


df_final = geojson.merge(df3, left_on="c_ar", right_on="arrondissement", how="outer") 


# On utilise plotly_express pour créer une carte interactive qui donne les prix moyen au mètre carré dans chaque arrondissement.

# In[13]:


import plotly.express as px

fig1 = px.choropleth_mapbox(df_final, locations = 'arrondissement',
                            featureidkey = 'properties.c_ar',
                            geojson= geojson,
                            color=df_final['prix du m2'],
                            color_continuous_scale="PuRd",
                            range_color=[8000,18000],
                            hover_name='arrondissement',
                            hover_data=['prix du m2'],
                            labels = {'arrondissement' : 'Arrondissement ', 
                                     'prix du m2' : 'prix du m2 '},
                            title="Prix moyen du m2 par arrondissement",
                            mapbox_style="open-street-map",
                            center= {'lat':48.866669, 'lon':2.33333},
                            zoom =10.5, 
                            opacity= 0.6)

fig1.show()


# In[ ]:




