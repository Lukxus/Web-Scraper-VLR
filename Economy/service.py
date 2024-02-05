def busca_economy(soup_partida, tipo_partida):
    if tipo_partida == 1:
        tbody_tags_tr = soup_partida.find_all("tbody")
        # Separando a primeira metade pois o codigo da tela de overview aparece antes da tela de economy
        tbody_tags_tr = tbody_tags_tr[(tipo_partida * 2) :]
        print(tbody_tags_tr)
