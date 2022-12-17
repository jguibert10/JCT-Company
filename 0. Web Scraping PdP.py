#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 10:05:13 2022

@author: charlesrollet
"""

import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import logging
from tqdm import tqdm
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

path = '/Users/charlesrollet/Desktop/chromedriver-2'
           
def main():
    parser = argparse.ArgumentParser() 
    parser.add_argument('--n', type=int, default=2,help='Number of items to search')
    parser.add_argument('--fn', type=str, default='Cadrillage.csv',help='name of the output CSV file')
    args = parser.parse_args()

    start = time.time()
    n = runImmoDataScrapping(n=args.n, filename= args.fn)
    duration = time.time()-start
    logger.info(f'Scrapped {n} items in {duration/60.} minutes. ({str(duration/n).split(".")[0]} seconds per it)')
    
def runImmoDataScrapping(n: int, filename: str):
    for i in range(250000,420030,8501):
        for j in range(800001,900050,5001):
            step_x=2
            step_y=48
            driver = webdriver.Chrome(path)
            url = f"https://www.immo-data.fr/explorateur/transaction/recherche?minprice=0&maxprice=5000000&minpricesquaremeter=0&maxpricesquaremeter=40000&propertytypes=1%2C2&minmonthyear=Janvier%202014&maxmonthyear=Juin%202022&nbrooms=1%2C2%2C3%2C4%2C5&minsurface=0&maxsurface=400&minsurfaceland=0&maxsurfaceland=50000&center={step_x+i*0.000001}%3B{step_y+j*0.000001}&zoom=14.5"
        
            driver.get(url)
            driver.implicitly_wait(6)
            colsInDetailsList = ['addresse','type_bien', 'prix', 'prix_m2', 'details']
            data = {colName : [] for colName in colsInDetailsList}
        
            elements = driver.find_elements(by=By.XPATH, value='//div[@class="flex flex-col gap-2 p-3"]')
            
            for element in tqdm(elements):
                driver.implicitly_wait(2)            
                addresse = element.find_element(by=By.XPATH, value='//p[@class="text-gray-700 font-bold truncate"]').text
                type_bien = element.find_element(by=By.XPATH, value='//p[@class="flex items-center text-sm text-gray-400"]').text
                prix = element.find_element(by=By.XPATH, value='//p[@class="text-primary-500 font-bold whitespace-nowrap"]').text
                prix_m2= element.find_element(by=By.XPATH, value='//p[@class="text-gray-400 text-xs text-right"]').text
                details = element.find_element(by=By.XPATH, value='//div[@class="flex gap-5"]').text
                
                data['addresse'].append(addresse)
                data['prix'].append(prix)
                data['type_bien'].append(type_bien)
                data['prix_m2'].append(prix_m2)
                data['details'].append(details)
        
            driver.close()
            if i==250000 and j==800001 : 
                df = pd.DataFrame(data) 
            else : 
                df=pd.concat([df,pd.DataFrame(data)],ignore_index=True)      

    df.to_csv(filename)
    return df.shape[0]

if __name__=='__main__':

    main()
    
global df
    
