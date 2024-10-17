from datetime import datetime
from Enums.roundsEnum import RoundsEnum
from Enums.tipoPartida import TipoPartida
import re
import pandas as pd


def busca_campeonato(soup_partida):
    elemento = soup_partida.find("div", class_="match-header-event-series").parent.text.replace("\t", "").strip()
    partes = elemento.split("\n")
    partes.pop(1)
    temp = "".join(partes[1:])
    partes[1] = temp
    partes.pop()
    return partes

def busca_date(soup_partida):
    date = soup_partida.find("div", class_="moment-tz-convert").get("data-utc-ts")
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")


def busca_patch(soup_partida):
    patch = soup_partida.find("div", style="margin-top: 4px;")
    if patch != None:
        patch = patch.text.strip().replace("\n", "").replace("\t", "")
    return patch


def busca_estatisticas(soup_partida, tipo_partida):
    # PONTO DE ATENÇÂO: Ao buscar o quadro de estatisticas na tela de overview o nome dos elementos se repete na tela de economia
    # Sempre tera dois elementos desse por mapa na tela de economia e dois por mapa na tela de overview
    # Não foi possivel pegar esses elemetos separados então teremos que tratar a metade dos itens achados em cada função
    tbody_tags_tr = soup_partida.find_all("tbody")
    # Separando a primeira metade pois o codigo da tela de overview aparece antes da tela de economy
    
    """
    Tratamento antigo; Essa linha de codigo abaixo foi removida devido a partidas MD3 estarem sendo lidas da seguinte forma:
    0 - time 1 mapa 1
    1 - time 2 mapa 1
    2 - time 1 overview
    3 - time 2 overview
    4 - time 1 mapa 2
    5 - time 1 mapa 2
    6 - time 1 mapa 3
    7 - time 2 mapa 3

    Apos verificar em varias partidas, verificamos que os indices 2 e 3 da lista tbody_tags_tr sempre carregam dados de all maps
    """
    #tbody_tags_tr = tbody_tags_tr[: (tipo_partida * 2)]
    tr = len(tbody_tags_tr)
    if tr == 2: #MD1
        tbody_tags_tr = tbody_tags_tr[: (tipo_partida * 2)]
    else:
        aux = []
        for ind in range(len(tbody_tags_tr)):
            if ind != 2 and ind != 3:
                aux.append(tbody_tags_tr[ind])
    matriz_stats = []  # vezes pois são dois times
    for i in range(len(tbody_tags_tr)):
        if i != 2 and i != 3:
            tr_tag = tbody_tags_tr[i].find_all("tr")
            td_tag = []
            player_stats_mapa = []
            for j in tr_tag:
                td_tag = j.find_all("td")
                stats_mapa = {}
                for element in range(len(td_tag)):
                    if element == 0:  # nome jogador
                        try:
                            stats_mapa["name"] = (
                                td_tag[element]
                                .text.strip()
                                .replace("\n", "")
                                .replace("\t", "")
                            )
                        except:
                            stats_mapa["name"] = None
                    elif element == 1:  # agente
                        try:
                            stats_mapa["agente"] = (
                                td_tag[element]
                                .find("img")
                                .get("alt")
                                .strip()
                                .replace("\n", "")
                                .replace("\t", "")
                            )
                        except:
                            stats_mapa["agente"] = None
                    elif element == 2:  # R
                        try:
                            R = (
                                td_tag[element]
                                .text.strip()
                                .replace("\n", "")
                                .replace("\t", "")
                            )
                            padrao = r"\d+\.\d{2}"
                            numeros_formatados = re.findall(padrao, R)
                            stats_mapa["r"] = {
                                "geral": numeros_formatados[0],
                                "ataque": numeros_formatados[1],
                                "defesa": numeros_formatados[2],
                            }
                        except:
                            stats_mapa["r"] = {
                                "geral": None,
                                "ataque": None,
                                "defesa": None,
                            }
                    elif element == 3:  # ACS
                        try:
                            ACS_span = td_tag[element].find_all("span")
                            ACS = [
                                span.text.strip().replace("\n", "").replace("\t", "")
                                for span in ACS_span
                            ]
                            stats_mapa["acs"] = {
                                "geral": ACS[1],
                                "ataque": ACS[2],
                                "defesa": ACS[3],
                            }
                        except:
                            stats_mapa["acs"] = {
                                "geral": None,
                                "ataque": None,
                                "defesa": None,
                            }
                    elif element == 4:  # K
                        try:
                            K_span = td_tag[element].find_all("span")
                            K = [
                                span.text.strip().replace("\n", "").replace("\t", "")
                                for span in K_span
                            ]
                            stats_mapa["k"] = {
                                "geral": K[1],
                                "ataque": K[2],
                                "defesa": K[3],
                            }
                        except:
                            stats_mapa["k"] = {
                                "geral": None,
                                "ataque": None,
                                "defesa": None,
                            }
                    elif element == 5:  # D
                        try:
                            D_span = td_tag[element].find_all("span")
                            D = [
                                span.text.strip().replace("\n", "").replace("\t", "")
                                for span in D_span
                                if "/" not in span
                            ]
                            # tem uma classe span antes; Dai so não consideramos ela;
                            # Esse elemento fica no meio de duas "/" que estão em tags span
                            # Assim precisamos tirar as barras como foi feito na condição do for
                            # Ao montar a string temos essa lista ['/16412/', '16412', '16', '4', '12']
                            # as duas primeiras posições são informações indesejadas então são descartadas
                            stats_mapa["d"] = {
                                "geral": D[2],
                                "ataque": D[3],
                                "defesa": D[4],
                            }
                        except:
                            stats_mapa["d"] = {
                                "geral": None,
                                "ataque": None,
                                "defesa": None,
                            }
                    elif element == 6:  # A
                        try:
                            A_span = td_tag[element].find_all("span")
                            A = [
                                span.text.strip().replace("\n", "").replace("\t", "")
                                for span in A_span
                            ]
                            stats_mapa["a"] = {
                                "geral": A[1],
                                "ataque": A[2],
                                "defesa": A[3],
                            }
                        except:
                            stats_mapa["a"] = {
                                "geral": None,
                                "ataque": None,
                                "defesa": None,
                            }
                    elif element == 7:  # KDA+/-
                        try:
                            KDA_MAISMENOS_span = td_tag[element].find_all("span")
                            KDA_MAISMENOS = [
                                span.text.strip().replace("\n", "").replace("\t", "")
                                for span in KDA_MAISMENOS_span
                            ]
                            stats_mapa["kda+-"] = {
                                "geral": KDA_MAISMENOS[1],
                                "ataque": KDA_MAISMENOS[2],
                                "defesa": KDA_MAISMENOS[3],
                            }
                        except:
                            stats_mapa["kda+-"] = {
                                "geral": None,
                                "ataque": None,
                                "defesa": None,
                            }
                    elif element == 8:  # KAST
                        try:
                            KAST_span = td_tag[element].find_all("span")
                            KAST = [
                                span.text.strip().replace("\n", "").replace("\t", "")
                                for span in KAST_span
                            ]
                            stats_mapa["kast"] = {
                                "geral": KAST[1],
                                "ataque": KAST[2],
                                "defesa": KAST[3],
                            }
                        except:
                            stats_mapa["kast"] = {
                                "geral": None,
                                "ataque": None,
                                "defesa": None,
                            }
                    elif element == 9:  # ADR
                        try:
                            ADR_span = td_tag[element].find_all("span")
                            ADR = [
                                span.text.strip().replace("\n", "").replace("\t", "")
                                for span in ADR_span
                            ]
                            stats_mapa["adr"] = {
                                "geral": ADR[1],
                                "ataque": ADR[2],
                                "defesa": ADR[3],
                            }
                        except:
                            stats_mapa["adr"] = {
                                "geral": None,
                                "ataque": None,
                                "defesa": None,
                            }
                    elif element == 10:  # HS%
                        try:
                            HS_span = td_tag[element].find_all("span")
                            HS = [
                                span.text.strip().replace("\n", "").replace("\t", "")
                                for span in HS_span
                            ]
                            stats_mapa["hs"] = {
                                "geral": HS[1],
                                "ataque": HS[2],
                                "defesa": HS[3],
                            }
                        except:
                            stats_mapa["k"] = {
                                "geral": None,
                                "ataque": None,
                                "defesa": None,
                            }
                    elif element == 11:  # FK
                        try:
                            FK_span = td_tag[element].find_all("span")
                            FK = [
                                span.text.strip().replace("\n", "").replace("\t", "")
                                for span in FK_span
                            ]
                            stats_mapa["fk"] = {
                                "geral": FK[1],
                                "ataque": FK[2],
                                "defesa": FK[3],
                            }
                        except:
                            stats_mapa["fk"] = {
                                "geral": None,
                                "ataque": None,
                                "defesa": None,
                            }
                    elif element == 12:  # FD
                        try:
                            FD_span = td_tag[element].find_all("span")
                            FD = [
                                span.text.strip().replace("\n", "").replace("\t", "")
                                for span in FD_span
                            ]
                            stats_mapa["fd"] = {
                                "geral": FD[1],
                                "ataque": FD[2],
                                "defesa": FD[3],
                            }
                        except:
                            stats_mapa["fd"] = {
                                "geral": None,
                                "ataque": None,
                                "defesa": None,
                            }
                    elif element == 13:  # FKFD+/-
                        try:
                            FKFD_MAISMENOS_span = td_tag[element].find_all("span")
                            FKFD_MAISMENOS = [
                                span.text.strip().replace("\n", "").replace("\t", "")
                                for span in FKFD_MAISMENOS_span
                            ]
                            stats_mapa["fkfd+-"] = {
                                "geral": FKFD_MAISMENOS[1],
                                "ataque": FKFD_MAISMENOS[2],
                                "defesa": FKFD_MAISMENOS[3],
                            }
                        except:
                            stats_mapa["fkfd+-"] = {
                                "geral": None,
                                "ataque": None,
                                "defesa": None,
                            }
                #dataframe = pd.DataFrame(data=stats_mapa)
                player_stats_mapa.append(stats_mapa)
            matriz_stats.append(player_stats_mapa)
    return matriz_stats


def busca_tipo_partida(soup_partida):
    div_tipoPartida = soup_partida.find_all("div", class_="match-header-vs-note")
    valor_obtido = div_tipoPartida[1].text.strip()
    valor_enum = None
    if valor_obtido == "Bo1":
        valor_enum = TipoPartida.BO1.value
    elif valor_obtido == "Bo3" or valor_obtido == "3 Maps":
        valor_enum = TipoPartida.BO3.value
    elif valor_obtido == "Bo5":
        valor_enum = TipoPartida.BO5.value
    elif valor_obtido == "2 Maps":
        valor_enum = TipoPartida.MAPS2.value
    return valor_enum


def busca_nome_times(soup_partida):
    listaNomes = [
        nome.text.strip().replace("\n", "").replace("\t", "")
        for nome in soup_partida.find_all("div", class_=["wf-title-med"])
    ]
    # print(listaNomes)
    # print("----------------------------")
    return listaNomes[0], listaNomes[1]


def busca_mapas(soup_partida, tipo_partida):
    mapas = []
    if tipo_partida > 1:
        barraMapas = soup_partida.find_all("div", class_="vm-stats-gamesnav-container")
        barraMapas = barraMapas[0]
        barraMapasAux = barraMapas.find_all(
            "div", class_=["vm-stats-gamesnav", "noselect"]
        )
        barraMapasAux = barraMapasAux[0]
        mapasDiv = barraMapasAux.find_all(
            "div", class_=["vm-stats-gamesnav-item", "js-map-switch"]
        )
        for i in range(1, len(mapasDiv)):
            mapa = mapasDiv[i].find("div").get_text(strip=True)[1:]
            mapas.append(mapa)
            # precisei colocar esse [1:] para não pegar o primeiro elemento pois um elemento span estava colocando o texto dele junto
    else:
        mapasDiv = soup_partida.find_all("div", class_="map")
        mapasDiv = mapasDiv[0]
        mapasAux = mapasDiv.find_all(
            "div",
            style="font-weight: 700; font-size: 20px; text-align: center; position: relative; margin-bottom: 3px;",
        )
        mapasAux = mapasAux[0]
        mapas.append(mapasAux.text.strip().split('\t')[0])
    return mapas


"""
É necessario desconsiderar a primeira posição da 
matriz_resultados pois ela guarda a informações sobre os logos de cada time
"""


def busca_rounds(soup_partida, tipo_partida):
    lista_rounds = []
    div_colunas_aux = soup_partida.find_all("div", class_="vlr-rounds-row-col")
    div_colunas = []
    for element in div_colunas_aux:
        if element.has_attr("title"):
            div_colunas.append(element)
    for i in div_colunas:
        vazio_tag = i.find("div", class_="rnd-sq")
        img_tag = i.find("div", class_="rnd-sq mod-win mod-ct") or i.find(
            "div", class_="rnd-sq mod-win mod-t"
        )
        if vazio_tag and img_tag:
            result = img_tag.find("img")
            if i.index(vazio_tag) < i.index(img_tag):
                lista_rounds.append(["", result])
            else:
                lista_rounds.append([result, ""])
    if tipo_partida != 1:
        lista_scores = [
            element.text for element in soup_partida.find_all("div", class_="score")
        ]
        res = []
        for i in range(0, len(lista_scores), 2):
            res.append(
                lista_rounds[: (int(lista_scores[i]) + int(lista_scores[i + 1]))]
            )
            lista_rounds = lista_rounds[
                (int(lista_scores[i]) + int(lista_scores[i + 1])) :
            ]
        lista_rounds = res
    return tranforma_rounds(lista_rounds, tipo_partida)


def tranforma_rounds(matriz, tipo_partida):
    lista_rounds = [[] for _ in range(tipo_partida)]
    if tipo_partida != 1:
        for i in range(len(matriz)):
            if matriz[i]:
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
        if matriz:
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
