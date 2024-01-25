
import utils
from dotenv import load_dotenv
import os

load_dotenv()
num_paginas = 1


lista_acessos_total = utils.le_paginas(os.getenv("BASE_URL"), num_paginas)
print(f"Existem urls repetidas: {not(len(set(lista_acessos_total)) == len(lista_acessos_total))}")
utils.le_partidas(os.getenv("BASE_URL"), lista_acessos_total)