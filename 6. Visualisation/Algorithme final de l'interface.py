# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 20:58:12 2022

@author: julie
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 10:09:17 2022

@author: julie
"""
# ======================== IMPORT préambule ========================
#package classique
import pandas as pd
import numpy as np

#package pour l'affichage graphique
import tkinter as tk
import tkinter.messagebox
import tkintermapview
import customtkinter
import tkcalendar
import geopandas
from geopy.geocoders import Nominatim 

#package pour la récupération des coordonnées des arrondissements de Paris
import geojson 
import folium
import webbrowser

# ======================== Préambule - Récupération coordonnées ========================
 
geo = geojson.load(open("arrondissements.geojson"))

coord_arr = []
poly_arr = []
for i in range(20):
    txt = 'poly' + str(i+1)
    coord_arr.append(txt)
    poly = list(geo["features"][i]["geometry"].values())[1][0]
    for k in range(len(poly)):
        poly[k][0], poly[k][1] = poly[k][1], poly[k][0]
    poly.append(poly[0])
    poly_arr.append(poly)

keys = coord_arr
values = poly_arr
dict_arr = dict(zip(keys, values))




# ======================== Début - AFFICHAGE ========================

customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("dark-blue") 


class App(customtkinter.CTk):

    WIDTH = 1080
    HEIGHT = 950
    
    def __init__(self):
        super().__init__()

        self.title("Welcome at JCT Company.py")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing) 

        # ======================== create two frames ========================

        # configure grid layout (2x1)
        
        self.grid_columnconfigure(0, weight = 0)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=100,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")
        
        self.frame_right = customtkinter.CTkFrame(master=self,
                                                 width=20,
                                                 corner_radius=0, 
                                                 fg_color = "transparent")
        self.frame_right.grid(row=0, column=2, sticky="nswe")

        
        # ============ Titre général du frame_left ============
        
        self.label_titre = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Paramètres du bien à estimer",
                                              font=("Roboto Medium", -25))
        self.label_titre.grid(row=0, column=0, columnspan=2, pady=20, padx=10, sticky="nswe")
    
    
        # ============ Insertion de l'adresse du bien et de son arrondissement ============

        self.entry_adresse = customtkinter.CTkEntry(master=self.frame_left,
                                            width=100,
                                            placeholder_text="Adresse du bien")     
        self.entry_adresse.grid(row=1, column=0, pady=30, padx=10, sticky="we")
        
        self.combobox_arrondissement = customtkinter.CTkComboBox(master=self.frame_left,
                                                    values=["75001", "75002", "75003", "75004", "75005", "75006", "75007", "75008", "75009", "75010","75011", "75012", "75013", "75014", "75015","75016", "75017", "75018", "75019", "75020"])
        self.combobox_arrondissement.grid(row=1, column=1, pady=30, padx=10, sticky="we")
        self.combobox_arrondissement.set("Arrondissement")
        
        
        # ============ Insertion de la surface du bien ============
        
        self.entry_surface = customtkinter.CTkEntry(master=self.frame_left,
                                            width=100,
                                            placeholder_text="Surface du bien (en m2)")
        self.entry_surface.grid(row=2, column=0, pady=30, padx=10, sticky="we")


        # ============ Précision du type de bien (maison ou appartement) ============

        self.radio_var = tkinter.IntVar(value=0)
        
        self.radio_button_appartement = customtkinter.CTkRadioButton(master=self.frame_left,text="Appartement",
                                                           variable=self.radio_var,
                                                           value=0)
        self.radio_button_appartement.grid(row=3, column=0,pady=30, padx=10, sticky="nswe")

        self.radio_button_maison = customtkinter.CTkRadioButton(master=self.frame_left, text="Maison",
                                                           variable=self.radio_var,
                                                           value=1)
        self.radio_button_maison.grid(row=3, column=0,pady=30, padx=150, sticky="nswe")


        # ============ Insertion du prix d'achat du bien ============

        self.entry_prix = customtkinter.CTkEntry(master=self.frame_left,
                                            width=150,
                                            placeholder_text="Prix d'achat du bien")      
        self.entry_prix.grid(row=6, column=0, pady=30, padx=10, sticky="we")
        
        # ============ Définition d'une pièce ============
        
        self.label_info = customtkinter.CTkLabel(master=self.frame_left,
                                                   text="Indiquez le nombre de pièces \n" + "(On considère comme étant une pièce tout endroit de plus de 9m2 \n" +
                                                   "les salles de bains et WC ne sont pas pris en compte)",
                                                   width=400,
                                                   corner_radius=6,  
                                                   fg_color=("white", "gray38"),
                                                   justify=tkinter.LEFT)
        self.label_info.grid(row=4, column=0, pady=30, padx=10, sticky="w")
        
        
        # ============ Compteur pour indiquer le nombre de pièces ============
        
        self.res_piece = customtkinter.CTkLabel(master=self.frame_left,text='0')
        self.res_piece.grid(row=4, column=1, padx=10, pady=50, sticky="ew")
        
        
        # ============ Création de deux boutons pour régler le nombre de pièces du bien ============
        def compteur_plus():
            a= int(self.res_piece.cget("text"))
            if a >= 50:
                a = a
            else:
                a = a+1
            self.res_piece.configure(text=str(a))
            global nbp #crée une variable globale qu'on peut appeler n'importe où dans le code
            nbp = a
        
        def compteur_moins():
            b = int(self.res_piece.cget("text"))
            if b==0:
                b=b
            else:
                b = b-1
            self.res_piece.configure(text=str(b))
            global nbp #crée une variable globale qu'on peut appeler n'importe où dans le code
            nbp = b

        self.bouton_compteur_plus = customtkinter.CTkButton(master=self.frame_left, text="+", width=26, 
                                                    height=26,
                                                    command=compteur_plus)
        self.bouton_compteur_plus.place(x=521,y=380)
        
        self.bouton_compteur_moins = customtkinter.CTkButton(master=self.frame_left, text="-", width=26, 
                                                    height=26,
                                                    command=compteur_moins)
        self.bouton_compteur_moins.place(x=471,y=380)
        

        # ============ Précision de la date du jour ============
        def calendrier():
            #date_today = ''
            self.cal = tkcalendar.Calendar(self, selectmode = 'day', year = 2022, month = 12, day = 25)
            self.cal.place(x=950, y=490)
            def grad_date():
                #self.label_mask = customtkinter.CTkLabel(self.frame_left, width = 10)
                #self.label_mask.grid(row=11, column=1, pady=10, padx=10)
                self.date = customtkinter.CTkLabel(self, text = "") 
                self.date.configure(text = self.cal.get_date()) 
                self.cal.destroy()
                self.button_date.destroy()
                global date_today
                self.date_today = self.date.cget("text")
                date_today = self.date_today
                #affichage de la date
                self.label_calendrier = customtkinter.CTkLabel(master=self.frame_left,
                                                            text=self.date_today,
                                                            font=("Roboto Medium", -12),
                                                            corner_radius=6)
                self.label_calendrier.place(x=360, y=485)
            
            self.button_date=customtkinter.CTkButton(self, text = "OK", command = grad_date)
            self.button_date.place(x=650, y=485)
        
        self.label_calendrier = customtkinter.CTkLabel(master=self.frame_left,
                                                    text="Veuillez entrez la date du jour",
                                                    font=("Roboto Medium", -16),
                                                    corner_radius=0)
        self.label_calendrier.grid(row=5, column=0, pady=30, padx=0)

        self.botondate=customtkinter.CTkButton(self.frame_left, text='Date du jour', command=calendrier)
        self.botondate.grid(row=5, column=1, pady=30, padx=10)

        # ============ Changement du mode couleur ============

        self.optionmenu = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance)
        self.optionmenu.grid(row=7, column=0, padx=10, pady=30, sticky="ew")

        
        # ======================== frame_right ========================
        # Création tabview droite
        
        self.tabview = customtkinter.CTkTabview(self, width=600)
        self.tabview.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Résultat")
        self.tabview.add("Description")
        self.tabview.tab("Résultat").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Description").grid_columnconfigure(0, weight=1)
        
        # Création frame dans tabview Résultat
        self.frame_right_up = customtkinter.CTkFrame(master=self.tabview.tab("Résultat"),
                                                 width=100,
                                                 corner_radius=0)
        self.frame_right_up.grid(row=0, column=0, sticky="nswe")
        
        self.frame_right = customtkinter.CTkFrame(master=self.tabview.tab("Résultat"),
                                                 width=20,
                                                 corner_radius=0, 
                                                 fg_color = "transparent")
        self.frame_right.grid(row=1, column=0, sticky="nswe")

        self.map= tkintermapview.TkinterMapView(master=self.frame_right_up, width=1000, height=450)
        self.map.set_position(48.857345 , 2.347999)
        self.map.set_zoom(12)
        self.map.grid(row=0, column=0, sticky="nswe", padx=(0, 0), pady=(0, 0))
        
        self.botonestimation=customtkinter.CTkButton(master=self.frame_right, text='Estimation', command=self.callback)
        self.botonestimation.grid(row=2, column=3, pady=10, padx=0)

        # Tabview description
        #logo = tk.PhotoImage(file="image_visualisation.png")
        #self.label_calendrier = customtkinter.CTkLabel(master=self.tabview.tab("Description"),
        #                                            corner_radius=0,
        #                                            image=logo)
        #self.label_calendrier.grid(row=0, column=0, pady=30, padx=0)
        

        self.map2 = tkintermapview.TkinterMapView(master=self.tabview.tab("Description"), width=1000, height=450)
        self.map2.set_position(48.857345 , 2.347999)
        self.map2.set_zoom(12)
        self.map2.grid(row=0, column=0, sticky="nswe", padx=(0, 0), pady=(0, 0))

    # ======================== Espace des fonctions ============
    def test(self):
        self.label_res = customtkinter.CTkLabel(master=self.frame_right,
                                                    text="3 mille euros",
                                                    font=("Roboto Medium", -14),
                                                    fg_color = 'transparent',
                                                    corner_radius=6)
        self.label_res.grid(row=1, column=0, pady=0, padx=100)
        
    def button_event(self):
        print("Button pressed")

    def change_appearance(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()
        
    def callback(self):
        # ======================== Récoltes des variables depuis l'interface ============
        arr=int(self.combobox_arrondissement.get())
        p=int(self.radio_var.get())
        s=int(self.entry_surface.get())
        k=int(self.res_piece.cget("text"))
        u=int(self.entry_prix.get())
        global date_today
        self.date_today = date_today
        self.adr = str(self.entry_adresse.get())
        self.geolocator = Nominatim(timeout=10, user_agent = "myGeolocator")
        self.adr = self.adr + ' ' + str(arr) + ' ' + 'PARIS'
        self.adr_point = self.geolocator.geocode(self.adr)
        self.lat_bien = self.adr_point.latitude
        self.lgt_bien = self.adr_point.longitude
        
        # ======================== Estimation ================
        columns = ['type_local', 'surface_reelle_bati', 'longitude', 'latitude',
               'trimestre_trimestre_1', 'trimestre_trimestre_2',
               'trimestre_trimestre_3', 'trimestre_trimestre_4', 'année_2018',
               'année_2019', 'année_2020', 'année_2021', 'année_2022',
               'année_antérieur_a_2018', 'nb_pieces_0', 'nb_pieces_1', 'nb_pieces_2',
               'nb_pieces_3', 'nb_pieces_4', 'nb_pieces_5', 'nb_pieces_6',
               'nb_pieces_7', 'nb_pieces_8', 'nb_pieces_more_than_9']
        lst = [[0]*24]
        
        lst[0][0] = p #type local
        lst[0][1] = s #surface
        lst[0][2] = self.lgt_bien
        lst[0][3] = self.lat_bien
        lst[0][14+k] = 1 #nb de pièces
        
        #Gestion des dates
        temp = [int(str(date_today).split('/')[i]) for i in range(len(str(date_today).split('/')))]
        #temp = [mois, jour, année]

        if temp[2] >= 18:
            lst[0][8+(temp[2]-18)]=1
        else:
            lst[0][13]=1 #années
        lst[0][4+(temp[0]-1)//3]=1 #trimestres
        
        #CREATION D'UN DATAFRAME d'une ligne pour la prédiction
        df_test_1row = pd.DataFrame(lst, columns=columns)

        mean_absolute_error, mean_squared_error, max_error, explained_variance, mean_poisson_deviance, predict = fit(X_train_st, X_test_st, Y_train, best_model_rf)

        res_estimateur = predict 
        #res_estimateur = 144000 si ca ne fonctionne pas pour voir un résultat
        prix_estime = res_estimateur
        
        # ======================== Affichage des résultats ============
        
        txt = '     ' + "Valeur estimée du bien :" + '   ' + \
            str(prix_estime) + "€" + "      "

        self.label_res = customtkinter.CTkLabel(master=self.frame_right,
                                                    text=txt,
                                                    font=("Roboto Medium", -14),
                                                    fg_color = 'transparent',
                                                    corner_radius=6)
        self.label_res.grid(row=1, column=0, pady=30, padx=0)
        
        plus_value_res = prix_estime - u
        txt = '     ' + 'Plus value estimée possible :' + '   ' + \
             str(plus_value_res) + "€" + '     '
            #str(plus_value_res) + ' ' + '€'
        self.label_res_pv = customtkinter.CTkLabel(master=self.frame_right,
                                                    text=txt,
                                                    font=("Roboto Medium", -14),
                                                    fg_color = 'transparent',
                                                    corner_radius=6)
        self.label_res_pv.grid(row=2, column=0, pady=0, padx=0)
        
        #carte Résultat
        self.map= tkintermapview.TkinterMapView(master=self.frame_right_up, width=1000, height=450)
        self.map.set_position(48.857345, 2.347999)
        self.map.set_zoom(12)
        self.map.grid(row=0, column=0, sticky="nswe", padx=(0, 0), pady=(0, 0))
        self.map.set_marker(self.lat_bien,self.lgt_bien)
        
        #carte Descritption
        
        self.map2 = tkintermapview.TkinterMapView(master=self.tabview.tab("Description"), width=1000, height=450)
        self.map2.set_position(48.857345 , 2.347999)
        self.map2.set_zoom(12)
        self.map2.grid(row=0, column=0, sticky="nswe", padx=(0, 0), pady=(0, 0))
        
        encodage_dict_arr = [7, 15, 4, 16, 19, 9, 5, 1, 6, 3, 0, 10, 13, 14, 2, 17, 8, 11, 12, 18]
        index_arr = encodage_dict_arr[(arr-75000)-1]
        polygon_1 = self.map2.set_polygon(list(dict_arr.values())[index_arr],
                                            fill_color=None,
                                            outline_color="green",
                                            border_width=5,
                                            #command=polygon_click,
                                            #name="switzerland_polygon"
                                            )
        # methods
        polygon_1.add_position(0, 0, index=5)
        polygon_1.remove_position(0, 0)
        #polygon_1.delete()
        
        #Affichage Description
        liste_prixm2 = [13490, 11910, 12700, 12170, 12610, 13950, 13080, 11730, 10800, 10160,\
                10320, 9720, 9210, 10070, 9950, 10950, 10320, 9670, 8900, 9170]
        txt = "Le {0}ème arrondissement de Paris a un prix moyen du mettre carré de {1}€.".format(str(arr-75000), liste_prixm2[arr-75000-1])
        self.label_res_pv = customtkinter.CTkLabel(master=self.tabview.tab("Description"),
                                                    text=txt,
                                                    font=("Roboto Medium", -14),
                                                    fg_color = 'transparent',
                                                    corner_radius=6)
        self.label_res_pv.grid(row=1, column=0, pady=10, padx=0)
    
        prix_m2_bien = prix_estime/s
        diff = prix_m2_bien - liste_prixm2[(arr-75000)-1]
        txt = "Votre bien a un prix du m2 de {}€.".format(int(prix_m2_bien))
        self.label_res_pv = customtkinter.CTkLabel(master=self.tabview.tab("Description"),
                                                    text=txt,
                                                    font=("Roboto Medium", -14),
                                                    fg_color = 'transparent',
                                                    corner_radius=6)
        self.label_res_pv.grid(row=2, column=0, pady=10, padx=0)
        if diff >= 0:
            txt = "Le prix au m2 de votre bien est {}€ supérieur au prix moyen du m2 de votre arrondissement.".format(int(abs(diff)))
        else:
            txt = "Le prix au m2 de votre bien est {}€ inférieur au prix moyen du m2 de votre arrondissement.".format(int(abs(diff)))
        self.label_res_pv = customtkinter.CTkLabel(master=self.tabview.tab("Description"),
                                                    text=txt,
                                                    font=("Roboto Medium", -14),
                                                    fg_color = 'transparent',
                                                    corner_radius=6)
        self.label_res_pv.grid(row=3, column=0, pady=10, padx=0)
if __name__ == "__main__":
    app = App()
    app.mainloop()
    
