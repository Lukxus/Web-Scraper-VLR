
import re

def busca_quadro_compras(soup_partida, tipo_partida):
    maps_buys_match = []
    div_table_compras = soup_partida.find_all("div", class_="vm-stats-game")
    div_table_compras = div_table_compras[:-1]
    for i in range(len(div_table_compras)):
        table_compras = div_table_compras[i].find_all("table", class_="wf-table-inset mod-econ")
        table_compras = table_compras[0]
        '''
        0 -> Primerio quadro
        1 -> legendas
        2 -> Segundo quadro
        '''
        tr_table_compras = table_compras.find_all("tr")
        buys_match_time1 = []
        buys_match_time2 = []
        for tr in range(len(tr_table_compras)):
            tds = tr_table_compras[tr].find_all("td")
            pattern = r'(\d+)\t*\(\s*(\d+)\s*\)'
            if tr == 0:
                continue
            elif tr == 1:
                for td in range(len(tds)):
                    if td == 0: #nome dos times
                        continue
                    if td == 1:
                        buys_match_time1.append([tds[td].text.strip().replace("\n", "").replace("\t", "")])
                    else:
                        matches = re.findall(pattern, tds[td].text.strip())
                        numbers_before_tab = [match[0] for match in matches]
                        numbers_in_parentheses = [match[1] for match in matches]
                        buys_match_time1.append([numbers_before_tab,numbers_in_parentheses])
            elif tr == 2:
                for td in range(len(tds)):
                    if td == 0: #nome dos times
                        continue
                    if td == 1:
                        buys_match_time2.append([tds[td].text.strip().replace("\n", "").replace("\t", "")])
                    else:
                        matches = re.findall(pattern, tds[td].text.strip())
                        numbers_before_tab = [match[0] for match in matches]
                        numbers_in_parentheses = [match[1] for match in matches]
                        buys_match_time2.append([numbers_before_tab,numbers_in_parentheses])
        maps_buys_match.append([buys_match_time1, buys_match_time2])
    return maps_buys_match   
