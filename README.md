# Prédiction du prix d'un bien immobilier en fonction de certaines de ses caractéristiques 

Bienvenue sur le Github de notre projet Python Pour le Data Scientist ! 

L'objectif du projet est de prédire le prix d'un bien immobilier en fonction de certaines de ses caractéristiques telles que sa surface, son nombre de pièces, sa date de vente, son type (appartement ou maison) et sa location à Paris. 

Notre projet ce divise en 6 étapes :

<img width="940" alt="Capture d’écran 2022-12-19 à 16 21 35" src="https://user-images.githubusercontent.com/103358913/208459531-c4c0501c-c86e-4dc7-b6fb-0589ec5883a6.png">


# 1. Récupération des données ou Web Scraping 

Nous avons tout d'abord décidé de récupérer des données à partir du site Immodata (https://www.immo-data.fr/) qui référencie des biens vendus en France en donnant certaines de leurs caractéristiques. Afin de collecter un nombre significatif de données, nous avons enfermé Paris dans un rectangle dont les sommets correspondent à des coordonnées puis diviser ce rectangle en 400 petits rectangles afin de cadriller la ville. 


<img width="818" alt="Capture d’écran 2022-12-19 à 16 02 40" src="https://user-images.githubusercontent.com/103358913/208455469-70942fb1-f314-49aa-8793-723e46a044ce.png">


Nous avons ainsi réussi à obtenir envrion 40.000 données qu'il nous a ensuite fallu traiter. 

# 2. Traitement des données issues du Web Scraping 

La base issue du Web Scraping comportait plusieurs irrégularités qu'il nous a fallu corriger. 

Tout d'abord, comme nous souhaitons nous concentrer uniquement sur les biens localisés à Paris, nous avons supprimé de la base tous les biens qui se situent en dehors. Puis nous avons dû créer de nouvelles colonnes pour distinguer les variables. Ensuite, nous avons effectué un test de vraissemblance afin de supprimer les données qui semblaient irrégulières au vu de leur prix de vente par rapport à la surface et aux tendances du marché parisien.

Enfin, nous avons converti l'adresse des biens en coordonnées géographiques grâce à geopandas afin d'utiliser des valeurs numériques et non des chaînes de caractères dans la modélisation. Voici la base obtenue nettoyée. 

<img width="790" alt="Capture d’écran 2022-12-19 à 16 12 37" src="https://user-images.githubusercontent.com/103358913/208457745-7125f42a-885d-4ebb-a981-e1d9f68566aa.png">



# 3. Preprocessing 

Notre base comporte à la fois des varibales catégorielles ainsi que des variables continues. Nous avons donc dû traiter les deux types de variables séparément. 

* Les variables catégorielle :



