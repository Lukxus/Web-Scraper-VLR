import re

def busca_quadro_jogadas(soup_partida, tipo_partida):
    if tipo_partida == 1:
        table_jogadas = soup_partida.find_all(
            "table", class_="wf-table-inset mod-adv-stats"
        )
        table_jogadas = table_jogadas[0]
        tr_table_jogadas = table_jogadas.find_all("tr")
        jogadas_mapa = []
        for tr in range(len(tr_table_jogadas)):
            if tr == 0:  # pula para não pegar os nomes das colunas
                continue
            td = tr_table_jogadas[tr].find_all("td")
            jogadas_player_mapa = []
            for element in range(len(td)):
                if element == 0:  # nome jogador
                    jogadas_player_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                    )
                elif element == 1:  # agente
                    jogadas_player_mapa.append(
                        str(td[element].find("img").get("src"))
                        .split("/")[-1]
                        .split(".")[0]
                    )
                elif element == 2:  # 2K
                    jogadas_player_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 3:  # 3K
                    jogadas_player_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 4:  # 4K
                    jogadas_player_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 5:  # 5K
                    jogadas_player_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 6:  # 1v1
                    jogadas_player_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 7:  # 1v2
                    jogadas_player_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 8:  # 1v3
                    jogadas_player_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 9:  # 1v4
                    jogadas_player_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 10:  # 1v5
                    jogadas_player_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 11:  # ECON
                    jogadas_player_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 12:  # PL
                    jogadas_player_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 13:  # DE
                        jogadas_player_mapa.append(
                            td[element].text.strip().replace("\n", "").replace("\t", "")
                            if td[element]
                            .text.strip()
                            .replace("\n", "")
                            .replace("\t", "")
                            != ""
                            else 0
                        )
            jogadas_mapa.append(jogadas_player_mapa)
        return [jogadas_mapa]
    else:
        jogadas_mapas = []
        table_jogadas = soup_partida.find_all(
            "table", class_="wf-table-inset mod-adv-stats"
        )
        for i in range(len(table_jogadas)):
            if i != 0:
                jogadas_mapa = []
                tr_table_jogadas = table_jogadas[i].find_all("tr")
                for tr in range(len(tr_table_jogadas)):
                    if tr == 0:  # pula para não pegar os nomes das colunas
                        continue
                    td = tr_table_jogadas[tr].find_all("td")
                    jogadas_player_mapa = []
                    for element in range(len(td)):
                        if element == 0:  # nome jogador
                            if td[element]:
                                jogadas_player_mapa.append(
                                    td[element].text.strip().replace("\n", "").replace("\t", "")
                                )
                            else:
                                jogadas_player_mapa("")
                        elif element == 1:  # agente
                            if td[element]:
                                jogadas_player_mapa.append(
                                    str(td[element].find("img").get("src"))
                                    .split("/")[-1]
                                    .split(".")[0]
                                )
                            else:
                                jogadas_player_mapa("")
                        elif element == 2:  # 2K
                            if td[element].find("div", class_="stats-sq wf-popable vm-perf-notable mod-d"):
                                valor = td[element].find("div", class_="stats-sq wf-popable vm-perf-notable mod-d").get_text()
                                valorNumero = re.search(r"\d", str(valor))
                                jogadas_player_mapa.append(
                                    valorNumero.group() if valorNumero.group() != "" else 0
                                )
                            else:
                                jogadas_player_mapa.append("")
                        elif element == 3:  # 3K
                            if td[element].find("div", class_="stats-sq wf-popable vm-perf-notable mod-c"):
                                valor = td[element].find("div", class_="stats-sq wf-popable vm-perf-notable mod-c").get_text()
                                valorNumero = re.search(r"\d", str(valor))
                                jogadas_player_mapa.append(
                                    valorNumero.group()
                                    if valorNumero.group() != ""
                                    else 0
                                )
                            else:
                                jogadas_player_mapa.append("")
                        elif element == 4:  # 4K
                            if td[element].find("div", class_="stats-sq wf-popable vm-perf-notable mod-b"):
                                valor = td[element].find("div", class_="stats-sq wf-popable vm-perf-notable mod-b").get_text()
                                valorNumero = re.search(r"\d", str(valor))
                                jogadas_player_mapa.append(
                                    valorNumero.group()
                                    if valorNumero.group() != ""
                                    else 0
                                )
                            else:
                                jogadas_player_mapa.append("")
                        elif element == 5:  # 5K
                            if td[element].find("div", class_="stats-sq wf-popable vm-perf-notable mod-a"):
                                valor = td[element].find("div", class_="stats-sq wf-popable vm-perf-notable mod-a").get_text()
                                valorNumero = re.search(r"\d", str(valor))
                                jogadas_player_mapa.append(
                                    valorNumero.group()
                                    if valorNumero.group() != ""
                                    else 0
                                )
                            else:
                                jogadas_player_mapa.append("")
                        elif element == 6:  # 1v1
                            if td[element].find("div", class_="stats-sq wf-popable vm-perf-notable mod-e"):
                                valor = td[element].find("div", class_="stats-sq wf-popable vm-perf-notable mod-e").get_text()
                                valorNumero = re.search(r"\d", str(valor))
                                jogadas_player_mapa.append(
                                    valorNumero.group()
                                    if valorNumero.group() != ""
                                    else 0
                                )
                            else:
                                jogadas_player_mapa.append("")
                        elif element == 7:  # 1v2
                            if td[element].find("div", class_="stats-sq wf-popable vm-perf-notable mod-d"):
                                valor = td[element].find("div", class_="stats-sq wf-popable vm-perf-notable mod-d").get_text()
                                valorNumero = re.search(r"\d", str(valor))
                                jogadas_player_mapa.append(
                                    valorNumero.group()
                                    if valorNumero.group() != ""
                                    else 0
                                )
                            else:
                                jogadas_player_mapa.append("")
                        elif element == 8:  # 1v3
                            if td[element].find("div", class_="stats-sq wf-popable vm-perf-notable mod-c"):
                                valor = td[element].find("div", class_="stats-sq wf-popable vm-perf-notable mod-c").get_text()
                                valorNumero = re.search(r"\d", str(valor))
                                jogadas_player_mapa.append(
                                    valorNumero.group()
                                    if valorNumero.group() != ""
                                    else 0
                                )
                            else:
                                jogadas_player_mapa.append("")
                        elif element == 9:  # 1v4
                            if td[element].find("div", class_="stats-sq wf-popable vm-perf-notable mod-b"):
                                valor = td[element].find("div", class_="stats-sq wf-popable vm-perf-notable mod-b").get_text()
                                valorNumero = re.search(r"\d", str(valor))
                                jogadas_player_mapa.append(
                                    valorNumero.group()
                                    if valorNumero.group() != ""
                                    else 0
                                )
                            else:
                                jogadas_player_mapa.append("")
                        elif element == 10:  # 1v5
                            if td[element].find("div", class_="stats-sq wf-popable vm-perf-notable mod-a"):
                                valor = td[element].find("div", class_="stats-sq wf-popable vm-perf-notable mod-a").get_text()
                                valorNumero = re.search(r"\d", str(valor))
                                jogadas_player_mapa.append(
                                    valorNumero.group()
                                    if valorNumero.group() != ""
                                    else 0
                                )
                            else:
                                jogadas_player_mapa.append("")
                        elif element == 11:  # ECON
                            if td[element]:
                                jogadas_player_mapa.append(
                                td[element].text.strip().replace("\n", "").replace("\t", "")
                                if td[element]
                                .text.strip()
                                .replace("\n", "")
                                .replace("\t", "")
                                != ""
                                else 0
                            )
                            else:
                                jogadas_player_mapa.append("")
                        elif element == 12:  # PL
                            if td[element]:
                                jogadas_player_mapa.append(
                                td[element].text.strip().replace("\n", "").replace("\t", "")
                                if td[element]
                                .text.strip()
                                .replace("\n", "")
                                .replace("\t", "")
                                != ""
                                else 0
                            )
                            else:
                                jogadas_player_mapa("")
                        elif element == 13:  # DE
                            if td[element]:
                                jogadas_player_mapa.append(
                                td[element].text.strip().replace("\n", "").replace("\t", "")
                                if td[element]
                                .text.strip()
                                .replace("\n", "")
                                .replace("\t", "")
                                != ""
                                else 0
                            )
                            else:
                                jogadas_player_mapa.append("")
                    jogadas_mapa.append(jogadas_player_mapa)
                jogadas_mapas.append(jogadas_mapa)
        #print(len(jogadas_mapas))
        return jogadas_mapas


def busca_quadro_all_kills(soup_partida, tipo_partida):
    if tipo_partida == 1:
        table_all_kills = soup_partida.find_all(
            "table", class_="wf-table-inset mod-matrix mod-normal"
        )
        table_all_kills = table_all_kills[0]
        tbody_table_all_kills = table_all_kills.find("tbody")
        tr_tbody_table_all_kills = tbody_table_all_kills.find_all("tr")
        listaTimeUM = []
        listaTimeDOIS = []
        confrontos = []
        for tr in range(len(tr_tbody_table_all_kills)):
            td = tr_tbody_table_all_kills[tr].find_all("td")
            for valor_td in range(len(td)):
                if tr == 0:
                    if td[valor_td].text.strip() != "":
                        listaTimeDOIS.append(
                            td[valor_td]
                            .text.strip()
                            .replace("\n", "")
                            .replace("\t", "")
                        )
                else:
                    if valor_td == 0:
                        listaTimeUM.append(
                            td[valor_td]
                            .text.strip()
                            .replace("\n", "")
                            .replace("\t", "")
                        )
                    else:
                        div_stats_sq = td[valor_td].find_all("div", class_="stats-sq")
                        confronto_MT = [
                            element.text.strip().replace("\n", "").replace("\t", "")
                            for element in div_stats_sq
                        ]
                        confrontos.append(confronto_MT[:2])
        lista_confrontos = [listaTimeUM, listaTimeDOIS, confrontos]
        return lista_confrontos
    else:
        table_all_kills = soup_partida.find_all(
            "table", class_="wf-table-inset mod-matrix mod-normal"
        )
        lista_confrontos = []
        for table in range(len(table_all_kills)):
            if table == 0:
                continue
            tbody_table_all_kills = table_all_kills[table].find("tbody")
            tr_tbody_table_all_kills = tbody_table_all_kills.find_all("tr")

            listaTimeUM = []
            listaTimeDOIS = []
            confrontos = []
            for tr in range(len(tr_tbody_table_all_kills)):
                td = tr_tbody_table_all_kills[tr].find_all("td")
                for valor_td in range(len(td)):
                    if tr == 0:
                        if td[valor_td].text.strip() != "":
                            listaTimeDOIS.append(
                                td[valor_td]
                                .text.strip()
                                .replace("\n", "")
                                .replace("\t", "")
                            )
                    else:
                        if valor_td == 0:
                            listaTimeUM.append(
                                td[valor_td]
                                .text.strip()
                                .replace("\n", "")
                                .replace("\t", "")
                            )
                        else:
                            div_stats_sq = td[valor_td].find_all(
                                "div", class_="stats-sq"
                            )
                            confronto_MT = [
                                element.text.strip().replace("\n", "").replace("\t", "")
                                for element in div_stats_sq
                            ]
                            confrontos.append(confronto_MT[:2])
            lista_confrontos.append([listaTimeUM, listaTimeDOIS, confrontos])
        return lista_confrontos
