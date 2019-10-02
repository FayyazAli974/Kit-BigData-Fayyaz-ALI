import wikipediaapi
import random

wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI)


page_fin = 'Philosophy'
page_debut = 'France'
distance = 1
distance_max = 10000


page_courant = page_debut
print(page_courant)
while distance < distance_max:
      page_py = wiki_wiki.page(page_courant)
      if page_py.links and (len(page_py.links)>=100):
          links = page_py.links
          
      nom_page = list(links.keys())[random.randint(0, len(links)-1)] 
      if not (nom_page.startswith('Category') or ('Wiki' in nom_page)):
          page_courant = nom_page
          
          
      #page_courant = list(links.keys())[3]
      print(page_courant)
      if page_courant == page_fin:
          print(distance)
          break
      else:
          distance = distance + 1