# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 10:09:17 2022

@author: julie
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 10:54:55 2022
@author: charlesrollet
"""

import tkinter
import tkinter.messagebox
import tkintermapview
import customtkinter
import tkcalendar
import geopandas
from geopy.geocoders import Nominatim 
import pandas as pd
import numpy as np

global df

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
        
        #self.frame_info_piece = customtkinter.CTkFrame(master=self.frame_left)
        #self.frame_info_piece.place(x=10, y=358)
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
            self.cal = tkcalendar.Calendar(self, selectmode = 'day', year = 2022, month = 10, day = 21)
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

        
        # ======================== frame_right_down ========================

        # Bouton central
        
        self.tabview = customtkinter.CTkTabview(self, width=600)
        self.tabview.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Résultat")
        self.tabview.add("Description")
        self.tabview.tab("Résultat").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Description").grid_columnconfigure(0, weight=1)
        
        
        
    # ======================== Espace des fonctions ============
    
    def button_event(self):
        print("Button pressed")

    def change_appearance(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()

    def calendrier(self):
        #date_today = ''
        self.cal = tkcalendar.Calendar(self.frame_right_down, selectmode = 'day', year = 2022, month = 10, day = 21) 
        self.place(x=350, y=480)
        def grad_date(self):
            #self.label_mask = customtkinter.CTkLabel(self.frame_left, width = 10)
            #self.label_mask.grid(row=11, column=1, pady=10, padx=10)
            self.date = customtkinter.CTkLabel(self.frame_left, text = "") 
            self.date.config(text = self.cal.get_date()) 
            self.cal.destroy()
            self.button_date.destroy()
            #global date_today
            #self.date_today = self.date.cget("text") 
        self.button_date=customtkinter.CTkButton(self.frame_right_down, text = "OK", command = grad_date)
        self.button_date.place(x=350, y=580)

    def compteur_plus(self):
        a= int(self.res_piece.text_label.cget("text"))
        if a >= 50:
            a = a
        else:
            a = a+1
        self.res_piece.set_text(str(a))
    
    def compteur_moins(self):
        b = int(self.res_piece.text_label.cget("text"))
        if b==0:
            b=b
        else:
            b = b-1
        self.res_piece.set_text(str(b))
        
    def callback(self):
        #variables
        #global date_today
        n=int(self.combobox_arrondissement.get())
        p=0#int(self.radio_button_appartement.get())
        s=int(self.entry_surface.get())
        k=int(self.res_piece.text_label.cget("text"))
        u=int(self.entry_prix.get())
        self.date_today = "10/10/22" #ligne importante variable locale = variable globale
        self.adr = str(self.entry_adresse.get())
        self.geolocator = Nominatim(timeout=10, user_agent = "myGeolocator")
        self.adr = self.adr + ' ' + str(n) + ' ' + 'PARIS'
        self.adr_point = self.geolocator.geocode(self.adr)
        self.lat_bien = self.adr_point.latitude
        self.lgt_bien = self.adr_point.longitude
        #self.res = estimateur(n, p, s, k, self.date_today, self.lat_bien, self.lgt_bien) #liste en 0:prix en 1:nb de bien comparés en 2:df_bien_pertinents  
        #self.label_mask = customtkinter.CTkLabel(self.frame_right_down, text="cocuou", bg='#65BFCD', width=345, height=10)
        #self.label_mask.pack
        #self.label_mask.place(x=100, y=100) #on masque les résultats précédents
        txt = 'Prix du bien actualisé :' + '   ' + \
            str(self.res[0]) + ' ' + '€'
        self.res_aff = customtkinter.CTkLabel(self.frame_right_down,txt, (10, 50), (0,0))
        txt = 'Nombre de biens comparés :' + '  '+ \
            str(self.res[1])
        self.ind_aff = customtkinter.CTkLabel(self.frame_right_down,txt, (10, 100), (0,0))
        plus_value_res = self.res[0] - u
        txt = 'Plus value estimée possible :' + '   ' + \
            str(plus_value_res) + ' ' + '€'
        self.plus_value = customtkinter.CTkLabel(self.frame_right_down,txt, (10, 150), (0,0))
        #carte
        self.map.set_marker(self.lat_bien,self.lgt_bien)
        df_pertinent = self.res[2]
        for i in range(len(df_pertinent.index)):
            self.map.set_marker(df_pertinent.iloc[i]['latitude'], df_pertinent.iloc[i]['longitude'], marker_color_circle='cyan', marker_color_outside='blue')


if __name__ == "__main__":
    app = App()
    app.mainloop()
    