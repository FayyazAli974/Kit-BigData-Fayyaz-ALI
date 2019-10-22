#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:56:07 2019

@author: fayyazali
"""

import pandas as pd
import requests

# Récupération table Products
products = pd.read_csv('products.csv', sep=';')
print(products)


# Copie de product dans product2
products2 = products.copy()
products2['infos'] = products2['infos'].replace({',': ' '})


############################
# Traitement des ingrédients
############################
# Remplissage à la main des ingrédients mentionnés dans product
Ingredients = ['gluten','sugar','peanut','milk','soja','egg','mustard','fish']

def el_inc(s):
    liste_inc = [];
    for el in s:
        if el in Ingredients:
            liste_inc.append(el);
            
    return liste_inc

# Traitement du split de la colonne infos:
df = products['infos'].apply(lambda x: x.replace(",", "").split()).apply(lambda x: el_inc(x))


# Traitement des vrais ou faux des produits
for Ing in Ingredients:
    products2[Ing] = False
    products2[Ing] = df.apply(lambda x: True if Ing in x else False)
    

del products2['infos']


print(products2.head(5))

######################################
# Traitement de la conversion Currency
######################################
currency = requests.get('https://api.exchangerate-api.com/v4/latest/EURO').json()

products2['Currency'] = ' '

# Fonction qui donne le pays et le code de la currency à partir de l'IP
def Pays_Ip(x):
    #Ip_api = requests.get('http://ip-api.com/json/'+x+'?fields=country')
    # Limité à 45 par minute
    Ip_api = requests.get('http://free.ipwhois.io/json/'+x)
    
    #print(Ip_api.status_code) 
    
    if Ip_api.status_code == 200:        
        try:
            Pays = Ip_api.json().get('country')
            Currency = Ip_api.json().get('currency_code')
        except:
            Pays = 'Inconnu'
            Currency = 'Inconnu'
    else: 
        Pays = 'Inconnu'
        Currency = 'Inconnu'
    
    return Currency 


products2['Currency'] =  products2['ip_address'].apply(lambda x: Pays_Ip(x))

# Fonction qui calcule le taux de change par rapport à l'euro
def taux(p):
    try:
        t = 1/currency['rates'][p]
    except:
        t = 1
    
    return t

products2['taux_change']=products2['Currency'].apply(lambda x: taux(x))

products2['price'] = products2.price.apply(lambda x: x.split()[0])

products2['price euros']=products2['price'].astype(float).mul(products2['taux_change'].astype(float))

list(products2.columns.values);
print(products2)

format_dict = {'price euros':'€{0:,.1f}'}
print(products2.reindex(columns=['username','ip_address','product','price','Currency','taux_change','price euros','gluten','sugar','peanut','milk','soja','egg','mustard','fish']).style.format(format_dict).hide_index())


