# Prédiction du prix d'un bien immobilier en fonction de certaines de ses caractéristiques 

#### Bienvenue sur le Github de notre projet Python Pour le Data Scientist ! 

L'objectif du projet est de prédire le prix d'un bien immobilier en fonction de certaines de ses caractéristiques telles que sa surface, son nombre de pièces, sa date de vente, son type (appartement ou maison) et sa location à Paris. 

#### Notre projet se divise en 6 étapes :

<img width="941" alt="Capture d’écran 2022-12-20 à 17 50 35" src="https://user-images.githubusercontent.com/103358913/208721459-287f3f30-0333-4e3c-ae60-d836f0d2359d.png">

#### Veuillez installer au préalable les packages non conventionnels suivant pour utiliser le reste du programme : 

```
pip install customtkinter
```

```
pip install tkcalendar
```

```
pip install tkintermapview
```
Si vous avez déjà l'habitude d'utiliser ces modules, téléchargez la dernière mise à jour : 
```
pip install customtkinter --upgrade
```

# 0. Annexe  : Travail préliminaire 

Avant de maîtriser les différents modèles, le travail de standardisation ou la technique du web scraping, nous avons travaillé sur une base gouvernementale que nous avons nettoyée puis utilisée dans un modèle classique linéaire avant de construire un premier interface mais qui comportait plusieurs problèmes. 

Nous avons tenu néanmoins à mettre ce code car nous estimons que ce travail a été loin d'être anodin dans la réalisation de notre projet final qui s'est construit au fil des mois. 

# 1. Récupération des données ou Web Scraping 

Nous avons tout d'abord décidé de récupérer des données à partir du site Immodata (https://www.immo-data.fr/) qui référencie des biens vendus en France en donnant certaines de leurs caractéristiques. Afin de collecter un nombre significatif de données, nous avons enfermé Paris dans un rectangle dont les sommets correspondent à des coordonnées puis diviser ce rectangle en 400 petits rectangles afin de cadriller la ville. 


<img width="818" alt="Capture d’écran 2022-12-19 à 16 02 40" src="https://user-images.githubusercontent.com/103358913/208455469-70942fb1-f314-49aa-8793-723e46a044ce.png">


Nous avons ainsi réussi à obtenir envrion 40.000 données qu'il nous a ensuite fallu traiter. 

# 2. Traitement des données issues du Web Scraping 

La base issue du Web Scraping comportait plusieurs irrégularités qu'il nous a fallu corriger. 

Tout d'abord, comme nous souhaitons nous concentrer uniquement sur les biens localisés à Paris, nous avons supprimé de la base tous les biens qui se situent en dehors. Puis nous avons dû créer de nouvelles colonnes pour distinguer les variables. Ensuite, nous avons effectué un test de vraisemblance afin de supprimer les données qui semblaient irrégulières au vu de leur prix de vente par rapport à la surface et aux tendances du marché parisien.

Enfin, nous avons converti l'adresse des biens en coordonnées géographiques grâce à geopandas afin d'utiliser des valeurs numériques et non des chaînes de caractères dans la modélisation. Voici la base obtenue nettoyée. 

<img width="790" alt="Capture d’écran 2022-12-19 à 16 12 37" src="https://user-images.githubusercontent.com/103358913/208457745-7125f42a-885d-4ebb-a981-e1d9f68566aa.png">

# 3. Statistiques descriptives

Après récupération de la base de données, nous avons réalisé une série de statistiques descriptives afin de décrire de façon synthétique et parlante les données immobilières pour mieux les analyser.

Dans un premier temps, nous avons ainsi modifié la base de données obtenues précédemment, en transformant les coordonnées géographiques de chaque bien en une adresse postale. Nous avons également rajouté certaines variables qui nous paraissaient judicieuses, telles que le prix du mètre carré pour chaque bien. De fait, nous avons alors réalisé une carte interactive de la ville de Paris, avec pour chaque arrondissement, le prix moyen (au mètre carré) auquel les biens immobiliers sont vendus. 

Nous avons aussi réalisé des études statistiques afin de vérifier la fiabilité et l’importance des données, ainsi que les corrélations entre chaque variables.

<img width="400" alt="Capture d’écran 2022-12-21 à 13 04 24" src="https://user-images.githubusercontent.com/103358913/208901490-34e59adb-2d63-4f24-a51e-36f7f64b8238.png"><img width="400" alt="Capture d’écran 2022-12-21 à 13 04 56" src="https://user-images.githubusercontent.com/103358913/208901508-e10f11c1-d5e7-49c3-b274-d81f4b265431.png">

# 4. Preprocessing 

Notre base comporte à la fois des varibales catégorielles ainsi que des variables continues. Nous avons donc dû traiter les deux types de variables séparément. 

* #### Les variables catégorielles :

Nous avions trois variables catégorielles : la date, le nombre de pièces et le type du bien. 

Pour traiter la date nous avons converti la colonne en datetime puis créé deux nouvelles colonnes contenant l'année de vente et le mois. Nous avons en effet estimé que le jour de vente n'aurait pas réellement d'impact sur l'estimation du prix. Puis nous avons regroupé les mois en trimestres pour gagner en pertinance et regroupées les années inférieures à 2018 pour éviter d'avoir des données trop anciennes. 

Concernant le nombre de pièces, nous avons décidé de regrouper tous les biens de plus de 9 pièces dans une seule modalité afin d'éviter tout bruit possible. 

Nous avons ensuite encodé ces variables grâce à get_dummies() qui les a converties en indicatrices. 

Pour le type du bien, nous avons utilisé LabelEncoder() pour le recoder en binaire. 

* #### Les variables continues : 

Nous avions trois varibales continues : la surface, la longitude et la latitude. 

Nous avons alors créé une fonction nous permettant de choisir le meilleur standardiseur parmis StandardScaler, MinMaxScaler, RobustScaler pour 6 modèles utilisés. Nous avons décidé de principalement prendre des regressor puisque nous estimons que notre modèle s'y prête davantage et que nous avons testé des Classifieur mais cela n'a rien donné de très concluant. Nous avons voulu quand même en garder un. Le standardiseur qui avait globalement les meilleurs performances a été Robust. 

* #### Résultat du meilleur standardisateur selon les modèles utilisés : 

|          | Decision Tree Method | Random Forest Method | K Neighbors Classifier |         SCV            | Logistic Regression | Linear Regression | 
|:--------:| :------------------: | :------------------: | :--------------------: | :--------------------: | :-----------------: | :---------------: |
| Robust   |          ❌          |          ✅          |           ❌           |          ✅           |         ❌          |        ✅         |
| Standard |          ✅          |          ❌          |           ✅           |          ❌           |         ✅          |        ❌         |
| MinMax   |          ❌          |          ❌          |           ❌           |          ❌           |         ❌          |        ❌         |




Nous avons ensuite obtenu une base apte à être utilisée pour notre modélisation que nous avons séparé aléatoirement en X_train, X_test, Y_train, Y_test. En réalité, on observe que la différence entre les standardisateurs est assez négligeable mais cette démarche nous a sembler intéressante dans le cadre du projet.  

# 5. Modélisation 

Après avoir choisi le meilleur standardiseur pour chaque modèle utilisé, nous avons créé une fonction permettant de déterminer les hyperparamètres optimaux de chaque modèle parmi ceux sélectionnés. Enfin, nous avons entrainé chacun des modèles selon le standardiseur et les hyperparamètres optimaux. 

* #### Résultats des modèles utilisés : 

|                       | Decision Tree Method | Random Forest Method | K Neighbors Regressor  |     SVC     | Logistic Regression | Linear Regression | 
|:---------------------:| :------------------: | :------------------: | :--------------------: | :---------: | :-----------------: | :---------------: |
| Score                 |         0.86         |         0.90         |          0.90          |             |         0.1         |      0,91         |      
| mean_absolute_error   |                      |                      |                        |             |                     |                   |
| mean_squared_error    |                      |                      |                        |             |                     |                   |
| max_error             |                      |                      |                        |             |                     |                   |
| explained_variance    |                      |                      |                        |             |                     |                   |
| mean_poisson_deviance |                      |                      |                        |             |                     |                   |

Ainsi, nous avons décidé de choisir le modèle Random Forest Regressor avec comme standardiseur Robust et comme hyperparamètres XXX pour estimer le prix d'un bien selon certaines de ses caractéristiques. 

# 6. Visualisation grâce à une interface graphique 

Pour rendre plus interactif notre projet, nous avons décidé de créer une interface graphique grâce à TkinterCustom, un module créé par Tom Schimansky que nous remercions pour sa contribution. Ainsi, on peut indiquer l'adresse du bien recherché avec son arrondissement (qui sera convertie en coordonnées géographiques), le type de bien grâce à un widget bouton, le nombre de pièces grâce à un compteur, la date du jour grâce à un calendrier, ainsi que le prix d'achat du bien si nous en sommes propriétaire et que nous souhaitons connaître son estimation. 

<img width="960" alt="image_resultat_final" src="https://user-images.githubusercontent.com/116661212/208918745-2d8c6e9b-dfe8-43d8-9be6-7e17ff35026c.png">

Lorsque toutes les caractéristiques sont remplies, il ne reste plus qu'à appuyer sur le bouton centrale qui affichera une carte avec la localisation du bien, le prix estimé et la plus value possible en cas de vente si la personne est propriétaire. Enfin, nous avons créé un deuxième onglet Description qui permet d'avoir des informations supplémentaires sur le prix au m2 de notre bien estimé en fonction du marché dans son arrondissement.

<img width="960" alt="image_description_finale" src="https://user-images.githubusercontent.com/116661212/208919057-e2c57cd1-e89d-4ffa-8b44-70bf8c3b0479.png">


