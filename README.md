# Prédiction du prix d'un bien immobilier en fonction de certaines de ses caractéristiques 

Bienvenue sur le Github de notre projet Python Pour le Data Scientist ! 

L'objectif du projet est de prédire le prix d'un bien immobilier en fonction de certaines de ses caractéristiques telles que sa surface, son nombre de pièces, sa date de vente, son type (appartement ou maison) et sa location à Paris. 

Notre projet ce divise en 6 étapes :

<img width="936" alt="Capture d’écran 2022-12-19 à 16 22 26" src="https://user-images.githubusercontent.com/103358913/208459710-92b73219-7eca-4baa-878a-7ea69f93f61a.png">

# 1. Récupération des données ou Web Scraping 

Nous avons tout d'abord décidé de récupérer des données à partir du site Immodata (https://www.immo-data.fr/) qui référencie des biens vendus en France en donnant certaines de leurs caractéristiques. Afin de collecter un nombre significatif de données, nous avons enfermé Paris dans un rectangle dont les sommets correspondent à des coordonnées puis diviser ce rectangle en 400 petits rectangles afin de cadriller la ville. 


<img width="818" alt="Capture d’écran 2022-12-19 à 16 02 40" src="https://user-images.githubusercontent.com/103358913/208455469-70942fb1-f314-49aa-8793-723e46a044ce.png">


Nous avons ainsi réussi à obtenir envrion 40.000 données qu'il nous a ensuite fallu traiter. 

# 2. Traitement des données issues du Web Scraping 

La base issue du Web Scraping comportait plusieurs irrégularités qu'il nous a fallu corriger. 

Tout d'abord, comme nous souhaitons nous concentrer uniquement sur les biens localisés à Paris, nous avons supprimé de la base tous les biens qui se situent en dehors. Puis nous avons dû créer de nouvelles colonnes pour distinguer les variables. Ensuite, nous avons effectué un test de vraissemblance afin de supprimer les données qui semblaient irrégulières au vu de leur prix de vente par rapport à la surface et aux tendances du marché parisien.

Enfin, nous avons converti l'adresse des biens en coordonnées géographiques grâce à geopandas afin d'utiliser des valeurs numériques et non des chaînes de caractères dans la modélisation. Voici la base obtenue nettoyée. 

<img width="790" alt="Capture d’écran 2022-12-19 à 16 12 37" src="https://user-images.githubusercontent.com/103358913/208457745-7125f42a-885d-4ebb-a981-e1d9f68566aa.png">

# 3. Statistiques descriptives 

# 4. Preprocessing 

Notre base comporte à la fois des varibales catégorielles ainsi que des variables continues. Nous avons donc dû traiter les deux types de variables séparément. 

* #### Les variables catégorielles :

Nous avions trois variables catégorielles : la date, le nombre de pièces et le type du bien. 

Pour traiter la date nous avons converti la colonne en datetime puis créé deux nouvelles colonnes contenant l'année de vente et le mois. Nous avons en effet estimé que le jour de vente n'aurait pas réellement d'impact sur l'estimation du prix. Puis nous avons regroupé les mois en demi-semestres pour gagner en pertinance. 

Concernant le nombre de pièces, nous avons décidé de recoder tous les biens de plus de 9 pièces en cet intitulé afin d'éviter tout bruit possible. 

Nous avons ensuite encoder ces variables grâce à get.dummies() qui les a converties en indicatrices. 

Pour le type du bien, nous les avons recodé en binaire grâce à LabelEncoder(). 

* #### Les variables continues : 

Nous avions trois varibales continues : la surface, la longitude et la latitude. 

Nous avons alors créé une fonction nous permettant de choisir le meilleur standardisateur parmis StandardScaler, MinMaxScaler, RobustScaler pour 6 modèles utilisés. Le standardisateur qui avait globalement les meilleurs performances a été (). 

Nous avons ensuite obtenu une base apte à être utilisée pour notre modélisation que nous avons séparé aléatoirement en X_train, X_test, Y_train, Y_test. 

# 5 Modélisation 

# 6 Visualisation grâce à une interface graphique 

Pour rendre plus interactif notre projet, nous avons décidé de créer une interface graphique grâce à TkinterCustom, un module créé par Tom Schimansky que nous remercions pour sa contribution. Ainsi, on peut indiquer l'adresse du bien rechercher avec son arrondissement (qui sera convertie en coordonnées géographiques), le type de bien grâce à un widget bouton, le nombre de pièces grâce à un compteur, la date du jour grâce à un calendirer, ainsi que le prix d'achat du bien si nous en sommes propriétaire et que nous souhaitons connaitre son estimation. 

Ajouter photo

Lorsque toutes les caractéristiques sont remplies, il ne reste plus qu'à appuyer sur le bouton centrale qui affichera une carte avec la localisation du bien et celle des biens comparés, le prix estimé et la plus value possible en cas de vente si la personne est propriétaire. Enfin un nouveau onglet sera accessible donnant des informations sur les biens de l'arrondissement où est localisé celui qui est recherché. (à voir)
