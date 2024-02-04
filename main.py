
import utils
from dotenv import load_dotenv
import os

load_dotenv()
num_paginas = int(os.getenv("NUMERO_PAGINAS"))


# lista_acessos_total = utils.le_paginas(os.getenv("BASE_URL"), num_paginas)
# print(f"Existem urls repetidas: {not(len(set(lista_acessos_total)) == len(lista_acessos_total))}")
# utils.le_partidas(os.getenv("BASE_URL"))

#tres mapas
#utils.le_partidas("https://www.vlr.gg/295197/fenerbah-e-esports-vs-regnum-carya-esports-challengers-league-2024-t-rkiye-birlik-split-1-regula/?game=153246&tab=overview")

#um mapa
#utils.le_partidas("https://www.vlr.gg/294459/ftw-le-a-fc-esports-vs-impulse-gw-challengers-league-2024-portugal-tempest-split-1-regular-seaso/?game=152861&tab=overview")


#teste rocha
utils.le_partidas("https://www.vlr.gg/286660/sentinels-vs-paper-rex-afreecatv-valorant-league-gf/")