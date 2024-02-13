import requests
from Economy.service import busca_quadro_compras, get_quadro_tipo_compra_por_round
from Enums.TipoPartida import TipoPartida
from Enums.RoundsEnum import RoundsEnum
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import threading


from Overview.service import (
    busca_date,
    busca_estatisticas,
    busca_mapas,
    busca_nome_times,
    busca_patch,
    busca_rounds,
    busca_tipo_partida,
)
from Performance.service import busca_quadro_all_kills, busca_quadro_jogadas


load_dotenv()

"""
O numero de pagina tem q ser pelo menos 2 para permitir
que pelo menos uma página seja lida
"""


def le_paginas(base_url, pagina_inicial=1, num_paginas=2, num_threads=1):
    resultados = []
    
    def le_paginas_thread(thread_id):
        acessos_thread = []
        for contador in range(pagina_inicial + thread_id, num_paginas, num_threads):
            url_pagina = f"{base_url}?page={contador}"
            print(f"\nThread {thread_id} acessando {url_pagina}")
            acessos_thread.extend(le_retangulos(url_pagina))  
        resultados.extend(acessos_thread)  # Adicionando os resultados à lista resultados
        return acessos_thread

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=le_paginas_thread, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # Espera que todas as threads terminem

    return resultados


def le_retangulos(url_pagina):
    matches = []
    req_pagina = requests.get(url_pagina)
    html_pagina = req_pagina.text
    soup_pagina = BeautifulSoup(html_pagina, "html5lib")
    # print(f"url_pagina = {url_pagina}")
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
        # print("url_partida", url_partida)
        partidas = le_partidas(url_partida)
        if partidas != -1:
            matches.append(partidas)

    return matches


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

    # Pegando data

    date = busca_date(soup_partida)
    # print(date)

    # pegando patch do jogo
    patch = busca_patch(soup_partida)
    # print(patch)
    if patch == None:
        return -1

    # Pegando nome dos times da partida
    nomePrimeiroTime, nomeSegundoTime = busca_nome_times(soup_partida)

    # Pegando tipo da partida
    tipo_partida = busca_tipo_partida(soup_partida)
    # print(tipo_partida)
    # Uma partida pode ter mais de um mapa; Assim eh necessario
    # percorrer cada DIV que possui a classe 'vm-stats-gamesnav-item js-map-switch mod-active'

    # Pegando Mapas
    mapas = busca_mapas(soup_partida, tipo_partida)
    # print(mapas)

    # Pegando rounds da partida
    rounds = busca_rounds(soup_partida, tipo_partida)
    # print(rounds)

    # Pegando quadro de estatisticas dos jogadores
    estatisticas = busca_estatisticas(soup_partida, tipo_partida)
    # # print(estatisticas)

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
    # print(quadro_all_kills)

    quadro_jogadas = busca_quadro_jogadas(soup_partida, tipo_partida)
    # print(quadro_jogadas)
    # # print(quadro_all_kills)

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
    # print(quadro_compras)

    quadro_tipo_compra_por_round = get_quadro_tipo_compra_por_round(
        soup_partida, tipo_partida
    )
    # print(quadro_tipo_compra_por_round)
    # ------------------
    # Fechando Economy
    # ------------------

    return {
        'date': date,
        'patch': patch,
        'nomePrimeiroTime': nomePrimeiroTime,
        'nomeSegundoTime': nomeSegundoTime,
        'tipo_partida': tipo_partida,
        'mapas': mapas,
        'rounds'  : rounds,
        'estatisticas' : estatisticas,
        'quadro_all_kills': quadro_all_kills,
        'quadro_jogadas' : quadro_jogadas,
        'quadro_compras' :quadro_compras,
        'quadro_tipo_compra_por_round' : quadro_tipo_compra_por_round
    }


def get_links_performance_economy(soup_partida):
    links = soup_partida.find_all("div", class_="vm-stats-tabnav")
    links = links[0]
    links_a = links.find_all("a")
    lista_links = []
    for a in links_a:
        lista_links.append(a["href"])
    return lista_links
