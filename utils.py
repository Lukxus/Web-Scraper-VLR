import requests
from Economy.service import busca_quadro_compras, get_quadro_tipo_compra_por_round
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import threading
import datetime
import time


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


def le_paginas(base_url, pagina_inicial=1, num_paginas=1, num_threads=1):
    resultados = []

    def le_pagina(url_pagina):
        print(f"\nAcessando {url_pagina}")
        return le_retangulos(url_pagina)

    def le_paginas_thread(start_page, end_page):
        acessos_thread = []
        for pagina in range(start_page, end_page + 1):
            url_pagina = f"{base_url}?page={pagina}"
            tentativas = 3  # número máximo de tentativas
            while tentativas > 0:
                try:
                    acessos_thread.extend(le_pagina(url_pagina))
                    time.sleep(0.001)
                    break  # Se não houve erro, sair do loop
                except Exception as e:
                    with open(os.getenv("CAMINHO_ERROS_TXT"), "a") as arquivo:
                        arquivo.write(f"Erro ao acessar {url_pagina}. Tentando novamente. Erro: {e} \n")
                    tentativas -= 1
            else:
                with open(os.getenv("CAMINHO_ERROS_TXT"), "a") as arquivo:
                    arquivo.write(f"Não foi possível acessar {url_pagina} após 3 tentativas.\n")

        resultados.extend(acessos_thread)
        return acessos_thread

    pages_per_thread = (num_paginas + num_threads - 1) // num_threads
    threads = []

    for i in range(num_threads):
        start_page = pagina_inicial + i * pages_per_thread
        end_page = min(
            pagina_inicial + (i + 1) * pages_per_thread - 1,
            pagina_inicial + num_paginas - 1,
        )
        try:
            thread = threading.Thread(target=le_paginas_thread, args=(start_page, end_page))
        except Exception as e:
            print(f"Erro ao criar thread: {e}")
        else:
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
    try:
        req_partida = requests.get(url_partida)
        html_partida = req_partida.text
        soup_partida = BeautifulSoup(html_partida, "html5lib")

        # ------------------
        # Acessando Overview
        # ------------------

        # Pegando data

        date = busca_date(soup_partida)

        # pegando patch do jogo
        patch = busca_patch(soup_partida)
        if patch == None:
            return -1

        # Pegando nome dos times da partida
        nomePrimeiroTime, nomeSegundoTime = busca_nome_times(soup_partida)

        # Pegando tipo da partida
        tipo_partida = busca_tipo_partida(soup_partida)

        # Pegando Mapas
        mapas = busca_mapas(soup_partida, tipo_partida)

        # Pegando rounds da partida
        rounds = busca_rounds(soup_partida, tipo_partida)

        # Pegando quadro de estatisticas dos jogadores
        estatisticas = busca_estatisticas(soup_partida, tipo_partida)

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
        quadro_jogadas = busca_quadro_jogadas(soup_partida, tipo_partida)

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
        # ------------------
        # Fechando Economy
        # ------------------

        return {
            "url": url_partida,
            "date": date,
            "patch": patch,
            "nomePrimeiroTime": nomePrimeiroTime,
            "nomeSegundoTime": nomeSegundoTime,
            "tipo_partida": tipo_partida,
            "mapas": mapas,
            "rounds": rounds,
            "estatisticas": estatisticas,
            "quadro_all_kills": quadro_all_kills,
            "quadro_jogadas": quadro_jogadas,
            "quadro_compras": quadro_compras,
            "quadro_tipo_compra_por_round": quadro_tipo_compra_por_round,
        }
    except Exception as e:
        with open(os.getenv("CAMINHO_ERROS_TXT"), "a") as arquivo:
            arquivo.write(url_partida + f" - {e}\n")
        return -1


def get_links_performance_economy(soup_partida):
    links = soup_partida.find_all("div", class_="vm-stats-tabnav")
    links = links[0]
    links_a = links.find_all("a")
    lista_links = []
    for a in links_a:
        lista_links.append(a["href"])
    return lista_links


def escreveHora(arq):
    data_e_hora_atual = datetime.datetime.now()
    data_e_hora_formatada = data_e_hora_atual.strftime("%d/%m/%Y %H:%M:%S")
    with open(f"{arq}", "a") as arquivo:
        arquivo.write(f"Execucao de {data_e_hora_formatada} \n\n")

def limpa_arquivos(arq):
    with open(f"{arq}", "w") as f:
        f.write("")
