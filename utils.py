import re
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

    #------------------
    #Acessando Overview
    #------------------

    #Pegando Mapas
    mapas = busca_mapas(soup_partida, tipo_partida)
    print(mapas)
    
    #Pegando rounds da partida
    rounds = busca_rounds(soup_partida, tipo_partida)
    print(rounds)
    
    #Pegando quadro de estatisticas dos jogadores
    estatisticas = busca_estatisticas(soup_partida, tipo_partida)
    print(estatisticas)

    #------------------
    #Fechando Overview
    #------------------

    #------------------
    #Acessando Performace
    #------------------

    exit(1)

def busca_estatisticas(soup_partida, tipo_partida):
    # PONTO DE ATENÇÂO: Ao buscar o quadro de estatisticas na tela de overview o nome dos elementos se repete na tela de economia
    # Sempre tera dois elementos desse por mapa na tela de economia e dois por mapa na tela de overview
    # Não foi possivel pegar esses elemetos separados então teremos que tratar a metade dos itens achados em cada função
    tbody_tags_tr = soup_partida.find_all('tbody')
    #Separando a primeira metade pois o codigo da tela de overview aparece antes da tela de economy
    tbody_tags_tr = tbody_tags_tr[:(tipo_partida*2)]
    matriz_stats = [[] for _ in range(tipo_partida * 2)] # vezes pois são dois times
    for i in range(len(tbody_tags_tr)):
        tr_tag = tbody_tags_tr[i].find_all("tr")
        td_tag = []
        player_stats_mapa = []
        for j in tr_tag:
            td_tag = j.find_all("td")
            stats_mapa = []
            for element in range(len(td_tag)):
                if element == 0:
                    #print(td_tag[element].text.strip().replace('\n', '').replace('\t', '')) #nome jogador
                    stats_mapa.append(td_tag[element].text.strip().replace('\n', '').replace('\t', ''))
                elif element == 1:
                    #print(td_tag[element].find('img').get('alt').strip().replace('\n', '').replace('\t', '')) # agente
                    stats_mapa.append(td_tag[element].find('img').get('alt').strip().replace('\n', '').replace('\t', ''))
                elif element == 2:
                    R = td_tag[element].text.strip().replace('\n', '').replace('\t', '') # R
                    padrao = r'\d+\.\d{2}'
                    numeros_formatados = re.findall(padrao, R)
                    #print(numeros_formatados)
                    stats_mapa.append(numeros_formatados)
                elif element == 3:
                    ACS_span = td_tag[element].find_all("span") # ACS
                    ACS = [span.text.strip().replace('\n', '').replace('\t', '') for span in ACS_span]
                    ACS = ACS[1:] # tem uma classe span antes; Dai so não consideramos ela
                    #print(ACS)
                    stats_mapa.append(ACS)
                elif element == 4:
                    K_span = td_tag[element].find_all("span") # K
                    K = [span.text.strip().replace('\n', '').replace('\t', '') for span in K_span]
                    K = K[1:] # tem uma classe span antes; Dai so não consideramos ela
                    #print(K)
                    stats_mapa.append(K)
                elif element == 5:
                    D_span = td_tag[element].find_all("span") # D
                    D = [span.text.strip().replace('\n', '').replace('\t', '') for span in D_span if '/' not in span]
                    D = D[2:] 
                    # tem uma classe span antes; Dai so não consideramos ela; 
                    # Esse elemento fica no meio de duas "/" que estão em tags span
                    # Assim precisamos tirar as barras como foi feito na condição do for
                    # Ao montar a string temos essa lista ['/16412/', '16412', '16', '4', '12']
                    # as duas primeiras posições são informações indesejadas então são descartadas
                    #print(D)
                    stats_mapa.append(D)
                elif element == 6:
                    A_span = td_tag[element].find_all("span") # A
                    A = [span.text.strip().replace('\n', '').replace('\t', '') for span in A_span]
                    A = A[1:] # tem uma classe span antes; Dai so não consideramos ela
                    #print(A)
                    stats_mapa.append(A)
                elif element == 7:
                    KDA_MAISMENOS_span = td_tag[element].find_all("span") # KDA+/-
                    KDA_MAISMENOS = [span.text.strip().replace('\n', '').replace('\t', '') for span in KDA_MAISMENOS_span]
                    KDA_MAISMENOS = KDA_MAISMENOS[1:] # tem uma classe span antes; Dai so não consideramos ela
                    #print(KDA_MAISMENOS)
                    stats_mapa.append(KDA_MAISMENOS)
                elif element == 8:
                    KAST_span = td_tag[element].find_all("span") # KAST
                    KAST = [span.text.strip().replace('\n', '').replace('\t', '') for span in KAST_span]
                    KAST = KAST[1:] # tem uma classe span antes; Dai so não consideramos ela
                    #print(KAST)
                    stats_mapa.append(KAST)
                elif element == 9:
                    ADR_span = td_tag[element].find_all("span") # ADR
                    ADR = [span.text.strip().replace('\n', '').replace('\t', '') for span in ADR_span]
                    ADR = ADR[1:] # tem uma classe span antes; Dai so não consideramos ela
                    #print(ADR)
                    stats_mapa.append(ADR)
                elif element == 10:
                    HS_span = td_tag[element].find_all("span") # HS%
                    HS = [span.text.strip().replace('\n', '').replace('\t', '') for span in HS_span]
                    HS = HS[1:] # tem uma classe span antes; Dai so não consideramos ela
                    #print(HS)
                    stats_mapa.append(HS)
                elif element == 11:
                    FK_span = td_tag[element].find_all("span") # FK
                    FK = [span.text.strip().replace('\n', '').replace('\t', '') for span in FK_span]
                    FK = FK[1:] # tem uma classe span antes; Dai so não consideramos ela
                    #print(FK)
                    stats_mapa.append(FK)
                elif element == 12:
                    FD_span = td_tag[element].find_all("span") # FD
                    FD = [span.text.strip().replace('\n', '').replace('\t', '') for span in FD_span]
                    FD = FD[1:] # tem uma classe span antes; Dai so não consideramos ela
                    #print(FD)
                    stats_mapa.append(FD)
                elif element == 13:
                    FKFD_MAISMENOS_span = td_tag[element].find_all("span") # FKFD+/-
                    FKFD_MAISMENOS = [span.text.strip().replace('\n', '').replace('\t', '') for span in FKFD_MAISMENOS_span]
                    FKFD_MAISMENOS = FKFD_MAISMENOS[1:] # tem uma classe span antes; Dai so não consideramos ela
                    #print(FKFD_MAISMENOS)
                    stats_mapa.append(FKFD_MAISMENOS)
            player_stats_mapa.append(stats_mapa)
        matriz_stats[i].append(player_stats_mapa)
    return matriz_stats

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
                        lista_rounds[0].append(RoundsEnum.EQUIPE2DESARMA.value)
                    elif "boom" in str(element[1]):
                        lista_rounds[0].append(RoundsEnum.EQUIPE2DETONA.value)
                    elif "time" in str(element[1]):
                        lista_rounds[0].append(RoundsEnum.EQUIPE2TEMPO.value)
                    elif "elim" in str(element[1]):
                        lista_rounds[0].append(RoundsEnum.EQUIPE2ELIMINA.value)
                else:
                    if "defuse" in str(element[0]):
                        lista_rounds[0].append(RoundsEnum.EQUIPE1DESARMA.value)
                    elif "boom" in str(element[0]):
                        lista_rounds[0].append(RoundsEnum.EQUIPE1DETONA.value)
                    elif "time" in str(element[0]):
                        lista_rounds[0].append(RoundsEnum.EQUIPE1TEMPO.value)
                    elif "elim" in str(element[0]):
                        lista_rounds[0].append(RoundsEnum.EQUIPE1ELIMINA.value)

    return lista_rounds
