import requests
import Enums.roundsEnum as roundsEnum
from bs4 import BeautifulSoup

def le_retangulos(url):
    lista_urls_partidas = []
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, "html5lib")
    
    for link in soup.find_all('a', class_=["wf-module-item", "match-item", "mod-color", "mod-left", "mod-bg-after-green"]):
        href = link.get('href')
        lista_urls_partidas.append(href)
    
    return lista_urls_partidas

def le_paginas(base_url, num_paginas):
    lista_acessos_total = []
    for contador in range(1, num_paginas):
        url_pagina = f"{base_url}?page={contador}"
        print(f"Contador: {contador}")
        lista_acessos_pagina = le_retangulos(url_pagina)
        lista_acessos_total.extend(lista_acessos_pagina)
    
    return lista_acessos_total

def le_partidas(base_url, lista_acessos):
  with open("url.txt", "w") as arquivo:
    arquivo.write("")
  with open("url.txt", "a") as arquivo:
    for acesso in lista_acessos:
        url = f"{base_url}{acesso}"
        print(url)
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, "html5lib")
        arquivo.write(url+'\n')

def tranforma_rounds(matriz):
   lista_rounds = [] 
   for element in matriz:
        if element[0] == None:
            if element[0] == "defuse":
                lista_rounds.append(roundsEnum.EQUIPE1DESARMA)
            elif element[0] == "boom":
                lista_rounds.append(roundsEnum.EQUIPE1DETONA)
            elif element[0] == "time":
                lista_rounds.append(roundsEnum.EQUIPE1TEMPO)
            elif element[0] == "elim":
                lista_rounds.append(roundsEnum.EQUIPE1ELIMINA)
        else:
            if element[0] == "defuse":
                lista_rounds.append(roundsEnum.EQUIPE2DESARMA)
            elif element[0] == "boom":
                lista_rounds.append(roundsEnum.EQUIPE2DETONA)
            elif element[0] == "time":
                lista_rounds.append(roundsEnum.EQUIPE2TEMPO)
            elif element[0] == "elim":
                lista_rounds.append(roundsEnum.EQUIPE2ELIMINA)