# Prédiction du prix d'un bien immobilier en fonction de certaines de ses caractéristiques 

Bienvenue sur le Github de notre projet Python Pour le Data Scientist ! 

L'objectif du projet est de prédire le prix d'un bien immobilier en fonction de certaines de ses caractéristiques telles que sa surface, son nombre de pièces, sa date de vente, son type (appartement ou maison) et sa location à Paris. 

Notre projet ce divise en 4 étapes :

# 1. Récupération des données ou Web Scraping 

Nous avons tout d'abord décidé de récupérer des données à partir du site Immodata (https://www.immo-data.fr/) qui référencie des biens vendus en France en donnant certaines de leurs caractéristiques. Afin de collecter un nombre significatif de données, nous avons enfermé Paris dans un rectangle dont les sommets correspondent à des coordonnées puis diviser ce rectangle en 400 petits rectangles afin de cadriller la ville. 


<img width="818" alt="Capture d’écran 2022-12-19 à 16 02 40" src="https://user-images.githubusercontent.com/103358913/208455469-70942fb1-f314-49aa-8793-723e46a044ce.png">


Nous avons ainsi réussi à obtenir envrion 40.000 données qu'il nous a ensuite fallu traiter. 

# 2. Traitement des données issues du Web Scraping 

La base issue du Web Scraping comportait plusieurs irrégularités qu'il nous a fallu corriger. Tout d'abord, comme nous souhaitons nous concentrer uniquement sur les biens localisés à Paris, nous avons supprimé de la base tous les biens qui se situent en dehors. Puis nous avons dû créer de nouvelles colonnes pour distinguer les variables. Enfin nous avons effectué un test de vraissemblance afin de supprimer les données qui semblaient irrégulières au vu de leur prix de vente par rapport à la surface et aux tendances du marché parisien.
