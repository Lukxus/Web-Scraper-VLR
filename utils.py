import requests
import Enums.roundsEnum as roundsEnum
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import Objetos.Partida as Partida

load_dotenv()

"""
O numero de pagina tem q ser pelo menos 2 para permitir
que pelo menos uma página seja lida
"""
def le_paginas(base_url, pagina_inicial = 1, num_paginas= 2):
    lista_acessos_total = []
    for contador in range(pagina_inicial, num_paginas):
        url_pagina = f"{base_url}?page={contador}"
        print(f"Contador: {contador}")
        lista_acessos_pagina = le_retangulos(url_pagina)
        lista_acessos_total.extend(lista_acessos_pagina)
    
    return lista_acessos_total

def le_retangulos(url_pagina):
    lista_urls_partidas = []
    req_pagina = requests.get(url_pagina)
    html_pagina = req_pagina.text
    soup_pagina = BeautifulSoup(html_pagina, "html5lib")
    print(f"url_pagina = {url_pagina}")
    # Iterando sobre todos os links de partidas encontrados na pagina
    for link in soup_pagina.find_all('a', class_=["wf-module-item", "match-item", "mod-color", "mod-left", "mod-bg-after-green"]):
        href = link.get('href')
        url_partida = f"{os.getenv('COMPLEMENTO_URL')}{href}"
        le_partidas(url_partida)
    
    return lista_urls_partidas


"""
Essa função sera responsavel por realizar a leitura 
de todas as informações presentes na página da partida;
Eh necessario fazer a divisao por Overview, Performace e Economy
"""
def le_partidas(url_partida):
    req_partida = requests.get(url_partida)
    html_partida = req_partida.text
    soup_partida = BeautifulSoup(html_partida, "html5lib")

    #Pegando nome dos times da partida
    nomePrimeiroTime, nomeSegundoTime = busca_nome_times(soup_partida)

    #Uma partida pode ter mais de um mapa; Assim eh necessario
    #percorrer cada DIV que possui a classe 'vm-stats-gamesnav-item js-map-switch mod-active'

    #Pegando Mapas
    mapas = busca_mapas(soup_partida)
    print(mapas)
    #Acessando Overview


    #Pegando rounds da partida
    # busca_rounds(soup_partida)

def busca_nome_times(soup_partida):
    listaNomes = [nome.text.strip() for nome in soup_partida.find_all('div', class_=["wf-title-med"])]
    print(listaNomes)
    print("----------------------------")
    return listaNomes[0], listaNomes[1]

"""
É necessario desconsiderar a primeira posição da 
matriz_resultados pois ela guarda a informações sobre os logos de cada time
"""
def busca_rounds(soup_partida):
    matriz_resultados_mapa = soup_partida.find_all('div', class_="map")
    matriz_resultados = soup_partida.find_all('div', class_=lambda x: x and 'vlr-rounds-row-col' in x.split())
    matriz_resultados_transformada = tranforma_rounds(matriz_resultados)
    

def busca_mapas(soup_partida):  
    barraMapas = soup_partida.find_all('div', class_= "vm-stats-gamesnav-container")
    barraMapas = barraMapas[0]
    barraMapasAux = barraMapas.find_all('div', class_=["vm-stats-gamesnav", "noselect"])
    barraMapasAux = barraMapasAux[0]
    mapasDiv =  barraMapasAux.find_all('div', class_=["vm-stats-gamesnav-item", "js-map-switch"])
    mapas = []
    for i in range(1, len(mapasDiv)):
        mapas.append(mapasDiv[i].find("div").get_text(strip=True)[1:]) 
        #precisei colocar esse [1:] para não pegar o primeiro elemento pois um elemento span estava colocando o texto dele junto
    return mapas

def tranforma_rounds(matriz_resultados):
    matriz_resultados = matriz_resultados[1:] # Remove o primeiro
    matriz_resultados_transformada = []
    for coluna in matriz_resultados:
        res = coluna.find_all('div', class_=["rnd-sq"])
        if res:
            print(res[0])
            print(res[1])
        else:
            print("lista vazia")
        #print(res)
        print("-------------------------------------")
    exit(0)


# def tranforma_rounds(matriz):
#    lista_rounds = [] 
#    for element in matriz:
#         if element[0] == None:
#             if element[0] == "defuse":
#                 lista_rounds.append(roundsEnum.EQUIPE1DESARMA)
#             elif element[0] == "boom":
#                 lista_rounds.append(roundsEnum.EQUIPE1DETONA)
#             elif element[0] == "time":
#                 lista_rounds.append(roundsEnum.EQUIPE1TEMPO)
#             elif element[0] == "elim":
#                 lista_rounds.append(roundsEnum.EQUIPE1ELIMINA)
#         else:
#             if element[0] == "defuse":
#                 lista_rounds.append(roundsEnum.EQUIPE2DESARMA)
#             elif element[0] == "boom":
#                 lista_rounds.append(roundsEnum.EQUIPE2DETONA)
#             elif element[0] == "time":
#                 lista_rounds.append(roundsEnum.EQUIPE2TEMPO)
#             elif element[0] == "elim":
#                 lista_rounds.append(roundsEnum.EQUIPE2ELIMINA)