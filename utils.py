import requests
from Economy.service import busca_quadro_compras
from Enums.TipoPartida import TipoPartida
from Enums.RoundsEnum import RoundsEnum
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

from Overview.service import (
    busca_estatisticas,
    busca_mapas,
    busca_nome_times,
    busca_rounds,
    busca_tipo_partida,
)
from Performance.service import busca_quadro_all_kills, busca_quadro_jogadas


load_dotenv()

"""
O numero de pagina tem q ser pelo menos 2 para permitir
que pelo menos uma página seja lida
"""


def le_paginas(base_url, pagina_inicial=1, num_paginas=2):
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
    for link in soup_pagina.find_all(
        "a",
        class_=[
            "wf-module-item",
            "match-item",
            "mod-color",
            "mod-left",
            "mod-bg-after-green",
        ],
    ):
        href = link.get("href")
        url_partida = f"{os.getenv('COMPLEMENTO_URL')}{href}"
        print("url_partida", url_partida)
        le_partidas(url_partida)

    return lista_urls_partidas


"""
Essa função sera responsavel por realizar a leitura 
de todas as informações presentes na página da partida;
Eh necessario fazer a divisao por Overview, Performace e Economy
"""


def le_partidas(url_partida):
    print(f"URL: {url_partida}")
    req_partida = requests.get(url_partida)
    html_partida = req_partida.text
    soup_partida = BeautifulSoup(html_partida, "html5lib")

    # ------------------
    # Acessando Overview
    # ------------------

    # Pegando nome dos times da partida
    nomePrimeiroTime, nomeSegundoTime = busca_nome_times(soup_partida)

    # Pegando tipo da partida
    tipo_partida = busca_tipo_partida(soup_partida)
    print(tipo_partida)
    # Uma partida pode ter mais de um mapa; Assim eh necessario
    # percorrer cada DIV que possui a classe 'vm-stats-gamesnav-item js-map-switch mod-active'

    # Pegando Mapas
    mapas = busca_mapas(soup_partida, tipo_partida)
    print(mapas)

    # Pegando rounds da partida
    rounds = busca_rounds(soup_partida, tipo_partida)
    print(rounds)

    # Pegando quadro de estatisticas dos jogadores
    estatisticas = busca_estatisticas(soup_partida, tipo_partida)
    # print(estatisticas)

    # ------------------
    # Fechando Overview
    # ------------------

    links_lista = get_links_performance_economy(soup_partida)
    link_performance = os.getenv("COMPLEMENTO_URL") + links_lista[1]
    link_economy = os.getenv("COMPLEMENTO_URL") + links_lista[2]

    # ------------------
    # Acessando Performace
    # ------------------
    req_partida = requests.get(link_performance)
    html_partida = req_partida.text
    soup_partida = BeautifulSoup(html_partida, "html5lib")

    quadro_all_kills = busca_quadro_all_kills(soup_partida, tipo_partida)
    print(quadro_all_kills)

    quadro_jogadas = busca_quadro_jogadas(soup_partida, tipo_partida)
    print(quadro_jogadas)
    # print(quadro_all_kills)

    # ------------------
    # Fechando Performace
    # ------------------

    # ------------------
    # Acessando Economy
    # ------------------
    req_partida = requests.get(link_economy)
    html_partida = req_partida.text
    soup_partida = BeautifulSoup(html_partida, "html5lib")

    quadro_compras = busca_quadro_compras(soup_partida, tipo_partida)
    print(quadro_compras)
    # ------------------
    # Fechando Economy
    # ------------------

    
    exit(1)


def get_links_performance_economy(soup_partida):
    links = soup_partida.find_all("div", class_="vm-stats-tabnav")
    links = links[0]
    links_a = links.find_all("a")
    lista_links = []
    for a in links_a:
        lista_links.append(a["href"])
    return lista_links
