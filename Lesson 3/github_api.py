#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 22:22:05 2019

@author: fayyazali
"""

import requests
import json
from bs4 import BeautifulSoup

# Put Credentials Here
identifiant = ''
token = ''


response = requests.get("https://gist.github.com/paulmillr/2657075")
soup = BeautifulSoup(response.text, 'html.parser')

user_table = soup.find_all('th', { 'scope' : 'row' })    

Tab_User = []
for user in user_table:
    link = user.find_next_sibling().text.split()[0]
    Tab_User.append(link)
    #print(link);          


print(len(Tab_User))


gh_session = requests.Session()
gh_session.auth = (identifiant, token)
dico = {}

i = 0
for user in Tab_User:   #['c9s','onevcat']:

    i = i+1
    print(i)
    #print(user)
    data0 = gh_session.get('https://api.github.com/users/'+user)
    data0 = data0.json()
    nombre_rep = data0['public_repos']
    #print(nombre_rep)
    
    star_moy = 0
    nombre_star = 0


    if nombre_rep !=0:
        nombre_pages = (nombre_rep//100)+1
        
        for p in range(nombre_pages):
            data = gh_session.get('https://api.github.com/users/'+user+'/repos?page='+str(p)+'&per_page=100')
            data = data.json()
            
            
            for rep in data:
                #print(rep['stargazers_count'])
                nombre_star = nombre_star + rep['stargazers_count']
                
            #print(nombre_star)
            star_moy = nombre_star/nombre_rep
    
    
    #print(nombre_star)
    
    dico[user] = star_moy


sorted_dico = sorted(dico.items(), key=lambda x: x[1], reverse=True)
print(sorted_dico)