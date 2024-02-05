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
                    jogadas_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                    )
                elif element == 1:  # agente
                    jogadas_mapa.append(
                        str(td[element].find("img").get("src"))
                        .split("/")[-1]
                        .split(".")[0]
                    )
                elif element == 2:  # 2K
                    jogadas_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 3:  # 3K
                    jogadas_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 4:  # 4K
                    jogadas_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 5:  # 5K
                    jogadas_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 6:  # 1v1
                    jogadas_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 7:  # 1v2
                    jogadas_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 8:  # 1v3
                    jogadas_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 9:  # 1v4
                    jogadas_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 10:  # 1v5
                    jogadas_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 11:  # ECON
                    jogadas_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
                elif element == 12:  # PL
                    jogadas_mapa.append(
                        td[element].text.strip().replace("\n", "").replace("\t", "")
                        if td[element].text.strip().replace("\n", "").replace("\t", "")
                        != ""
                        else 0
                    )
            jogadas_mapa.append(jogadas_player_mapa)
        return [jogadas_mapa]
    else:
        jogadas_mapas = []
        for i in range(tipo_partida):
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
                jogadas__player_mapa = []
                for element in range(len(td)):
                    if element == 0:  # nome jogador
                        jogadas_mapa.append(
                            td[element].text.strip().replace("\n", "").replace("\t", "")
                        )
                    elif element == 1:  # agente
                        jogadas_mapa.append(
                            str(td[element].find("img").get("src"))
                            .split("/")[-1]
                            .split(".")[0]
                        )
                    elif element == 2:  # 2K
                        jogadas_mapa.append(
                            td[element].text.strip().replace("\n", "").replace("\t", "")
                            if td[element]
                            .text.strip()
                            .replace("\n", "")
                            .replace("\t", "")
                            != ""
                            else 0
                        )
                    elif element == 3:  # 3K
                        jogadas_mapa.append(
                            td[element].text.strip().replace("\n", "").replace("\t", "")
                            if td[element]
                            .text.strip()
                            .replace("\n", "")
                            .replace("\t", "")
                            != ""
                            else 0
                        )
                    elif element == 4:  # 4K
                        jogadas_mapa.append(
                            td[element].text.strip().replace("\n", "").replace("\t", "")
                            if td[element]
                            .text.strip()
                            .replace("\n", "")
                            .replace("\t", "")
                            != ""
                            else 0
                        )
                    elif element == 5:  # 5K
                        jogadas_mapa.append(
                            td[element].text.strip().replace("\n", "").replace("\t", "")
                            if td[element]
                            .text.strip()
                            .replace("\n", "")
                            .replace("\t", "")
                            != ""
                            else 0
                        )
                    elif element == 6:  # 1v1
                        jogadas_mapa.append(
                            td[element].text.strip().replace("\n", "").replace("\t", "")
                            if td[element]
                            .text.strip()
                            .replace("\n", "")
                            .replace("\t", "")
                            != ""
                            else 0
                        )
                    elif element == 7:  # 1v2
                        jogadas_mapa.append(
                            td[element].text.strip().replace("\n", "").replace("\t", "")
                            if td[element]
                            .text.strip()
                            .replace("\n", "")
                            .replace("\t", "")
                            != ""
                            else 0
                        )
                    elif element == 8:  # 1v3
                        jogadas_mapa.append(
                            td[element].text.strip().replace("\n", "").replace("\t", "")
                            if td[element]
                            .text.strip()
                            .replace("\n", "")
                            .replace("\t", "")
                            != ""
                            else 0
                        )
                    elif element == 9:  # 1v4
                        jogadas_mapa.append(
                            td[element].text.strip().replace("\n", "").replace("\t", "")
                            if td[element]
                            .text.strip()
                            .replace("\n", "")
                            .replace("\t", "")
                            != ""
                            else 0
                        )
                    elif element == 10:  # 1v5
                        jogadas_mapa.append(
                            td[element].text.strip().replace("\n", "").replace("\t", "")
                            if td[element]
                            .text.strip()
                            .replace("\n", "")
                            .replace("\t", "")
                            != ""
                            else 0
                        )
                    elif element == 11:  # ECON
                        jogadas_mapa.append(
                            td[element].text.strip().replace("\n", "").replace("\t", "")
                            if td[element]
                            .text.strip()
                            .replace("\n", "")
                            .replace("\t", "")
                            != ""
                            else 0
                        )
                    elif element == 12:  # PL
                        jogadas_mapa.append(
                            td[element].text.strip().replace("\n", "").replace("\t", "")
                            if td[element]
                            .text.strip()
                            .replace("\n", "")
                            .replace("\t", "")
                            != ""
                            else 0
                        )
                jogadas_mapa.append(jogadas__player_mapa)
            jogadas_mapas.append(jogadas_mapa)
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
