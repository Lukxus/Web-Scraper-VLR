import requests
from Enums.TipoPartida import TipoPartida
from Enums.RoundsEnum import RoundsEnum
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
        print("url_partida",url_partida)
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

    #Pegando tipo da partida
    tipo_partida = busca_tipo_partida(soup_partida)
    print(tipo_partida)
    #Uma partida pode ter mais de um mapa; Assim eh necessario
    #percorrer cada DIV que possui a classe 'vm-stats-gamesnav-item js-map-switch mod-active'

    #Pegando Mapas
    mapas = busca_mapas(soup_partida, tipo_partida)
    print(mapas)
    #Acessando Overview
    
    #Pegando rounds da partida
    rounds = busca_rounds(soup_partida, tipo_partida)
    print(rounds)
    exit(1)

def busca_tipo_partida(soup_partida):
    div_tipoPartida = soup_partida.find_all('div', class_= 'match-header-vs-note')
    valor_obtido = div_tipoPartida[1].text.strip()
    valor_enum = None
    if valor_obtido == "Bo1":
        valor_enum = TipoPartida.BO1.value
    elif valor_obtido == "Bo3":
        valor_enum = TipoPartida.BO3.value
    elif valor_obtido == "Bo5":
        valor_enum = TipoPartida.BO5.value
    return valor_enum

def busca_nome_times(soup_partida):
    listaNomes = [nome.text.strip() for nome in soup_partida.find_all('div', class_=["wf-title-med"])]
    print(listaNomes)
    print("----------------------------")
    return listaNomes[0], listaNomes[1]

def busca_mapas(soup_partida, tipo_partida):
    mapas = []  
    if tipo_partida > 1:
        barraMapas = soup_partida.find_all('div', class_= "vm-stats-gamesnav-container")
        barraMapas = barraMapas[0]
        barraMapasAux = barraMapas.find_all('div', class_=["vm-stats-gamesnav", "noselect"])
        barraMapasAux = barraMapasAux[0]
        mapasDiv =  barraMapasAux.find_all('div', class_=["vm-stats-gamesnav-item", "js-map-switch"])
        for i in range(1, len(mapasDiv)):
            mapas.append(mapasDiv[i].find("div").get_text(strip=True)[1:]) 
            #precisei colocar esse [1:] para não pegar o primeiro elemento pois um elemento span estava colocando o texto dele junto
    else:
        mapasDiv =  soup_partida.find_all('div', class_="map")
        mapasDiv =  mapasDiv[0]
        mapasAux = mapasDiv.find_all('div', style="font-weight: 700; font-size: 20px; text-align: center; position: relative; margin-bottom: 3px;")
        mapasAux = mapasAux[0]
        mapas.append(mapasAux.text.strip())
    return mapas


"""
É necessario desconsiderar a primeira posição da 
matriz_resultados pois ela guarda a informações sobre os logos de cada time
"""
def busca_rounds(soup_partida, tipo_partida):
    lista_rounds = []
    div_colunas_aux = soup_partida.find_all('div', class_='vlr-rounds-row-col')
    div_colunas = []
    for element in div_colunas_aux:
        if element.has_attr("title"):
            div_colunas.append(element)
    for i in div_colunas:
        vazio_tag = i.find('div', class_='rnd-sq')
        img_tag = i.find('div', class_='rnd-sq mod-win mod-ct') or i.find('div', class_='rnd-sq mod-win mod-t')
        if vazio_tag and img_tag:
            result = img_tag.find('img')
            if i.index(vazio_tag) < i.index(img_tag):
                lista_rounds.append(["", result])
            else:
                lista_rounds.append([result, ""])
    if tipo_partida != 1:
        lista_scores = [element.text for element in soup_partida.find_all('div', class_='score')]
        res = []
        for i in range(0, len(lista_scores), 2):
            res.append(lista_rounds[:(int(lista_scores[i]) + int(lista_scores[i+1]))])
            lista_rounds = lista_rounds[:(int(lista_scores[i]) + int(lista_scores[i+1]))]
        lista_rounds = res[:]
    return tranforma_rounds(lista_rounds, tipo_partida)


def tranforma_rounds(matriz, tipo_partida):
    lista_rounds = [[] for _ in range(tipo_partida)] 
    if tipo_partida != 1:
        for i in range(tipo_partida):
            for element in matriz[i]:
                if element[0] == "":
                    if "defuse" in str(element[1]):
                        lista_rounds[i].append(RoundsEnum.EQUIPE2DESARMA.value)
                    elif "boom" in str(element[1]):
                        lista_rounds[i].append(RoundsEnum.EQUIPE2DETONA.value)
                    elif "time" in str(element[1]):
                        lista_rounds[i].append(RoundsEnum.EQUIPE2TEMPO.value)
                    elif "elim" in str(element[1]):
                        lista_rounds[i].append(RoundsEnum.EQUIPE2ELIMINA.value)
                else:
                    if "defuse" in str(element[0]):
                        lista_rounds[i].append(RoundsEnum.EQUIPE1DESARMA.value)
                    elif "boom" in str(element[0]):
                        lista_rounds[i].append(RoundsEnum.EQUIPE1DETONA.value)
                    elif "time" in str(element[0]):
                        lista_rounds[i].append(RoundsEnum.EQUIPE1TEMPO.value)
                    elif "elim" in str(element[0]):
                        lista_rounds[i].append(RoundsEnum.EQUIPE1ELIMINA.value)
    else:
        for element in matriz:
                if element[0] == "":
                    if "defuse" in str(element[1]):
                        lista_rounds.append(RoundsEnum.EQUIPE2DESARMA.value)
                    elif "boom" in str(element[1]):
                        lista_rounds.append(RoundsEnum.EQUIPE2DETONA.value)
                    elif "time" in str(element[1]):
                        lista_rounds.append(RoundsEnum.EQUIPE2TEMPO.value)
                    elif "elim" in str(element[1]):
                        lista_rounds.append(RoundsEnum.EQUIPE2ELIMINA.value)
                else:
                    if "defuse" in str(element[0]):
                        lista_rounds.append(RoundsEnum.EQUIPE1DESARMA.value)
                    elif "boom" in str(element[0]):
                        lista_rounds.append(RoundsEnum.EQUIPE1DETONA.value)
                    elif "time" in str(element[0]):
                        lista_rounds.append(RoundsEnum.EQUIPE1TEMPO.value)
                    elif "elim" in str(element[0]):
                        lista_rounds.append(RoundsEnum.EQUIPE1ELIMINA.value)

    return lista_rounds
