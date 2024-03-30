
import re
from Enums.CompraEnum import CompraEnum

def busca_quadro_compras(soup_partida, tipo_partida):
    maps_buys_match = []
    div_table_compras = soup_partida.find_all("div", class_="vm-stats-game")
    div_table_compras = div_table_compras[:-1]
    div_table_compras = [element for element in div_table_compras if element.text.strip().replace("\n", "").replace("\t", "") != "Stats from this map are not available yet"]
    for i in range(len(div_table_compras)):
        table_compras = div_table_compras[i].find_all("table", class_="wf-table-inset mod-econ")
        table_compras = table_compras[0]
        '''
        0 -> Primerio quadro
        1 -> Segundo quadro
        2 -> legendas
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


def get_quadro_tipo_compra_por_round(soup_partida, tipo_partida):
    info_round_map_match = []
    table = soup_partida.find_all("table", class_="wf-table-inset mod-econ")
    for i in range(len(table)):    
        if  i % 2 != 0:
            tr_table = table[i].find_all("tr")
            info_round_map = []
            while(tr_table):
                td_tr_table = tr_table[0].find_all("td")
                for td in range(len(td_tr_table)):
                    if td == 0:
                        continue
                    info_round_map.append([
                        [transforma_valor_com_K(element.text.strip().replace("\n", "").replace("\t", "")) for element in td_tr_table[td].find_all("div", class_="bank")],
                        [transforma_cat_compras(element.text.strip().replace("\n", "").replace("\t", "")) for element in td_tr_table[td].find_all("div", class_="rnd-sq")]
                    ])
                tr_table.pop(0)
            info_round_map_match.append(info_round_map)
    return info_round_map_match
            

def transforma_valor_com_K(valor):
    if valor[-1] == 'k':
        return float(valor[:-1]) * 1000
    
def transforma_cat_compras(valor):
    if valor == '':
        return CompraEnum.ECO.value
    elif valor == "$":
        return CompraEnum.SEMIECO.value
    elif valor == '$$':
        return CompraEnum.SEMIBUY.value
    elif valor == "$$$":    
        return CompraEnum.FULLBUY.value