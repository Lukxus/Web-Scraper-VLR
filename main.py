import utils
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
num_paginas = int(os.getenv("NUMERO_PAGINAS"))

# print(f"Existem urls repetidas: {not(len(set(lista_acessos_total)) == len(lista_acessos_total))}")
#utils.le_partidas(os.getenv("BASE_URL"))

# tres mapas
#utils.le_partidas("https://www.vlr.gg/295197/fenerbah-e-esports-vs-regnum-carya-esports-challengers-league-2024-t-rkiye-birlik-split-1-regula/?game=153246&tab=overview")

#um mapa
#utils.le_partidas("https://www.vlr.gg/294459/ftw-le-a-fc-esports-vs-impulse-gw-challengers-league-2024-portugal-tempest-split-1-regular-seaso/?game=152861&tab=overview")


# teste rocha
# utils.le_partidas(
#      "https://www.vlr.gg/286660/sentinels-vs-paper-rex-afreecatv-valorant-league-gf/"
#  )


#teste vazio
#utils.le_partidas("https://www.vlr.gg/299102/mesos-millionaires-vs-hyperspeed-ruby-game-changers-2024-north-america-series-1-ro24/?game=158270&tab=overview")


#teste partida vazia
#utils.le_partidas("https://www.vlr.gg/299956/fisher-rising-vs-nameless-challengers-league-2024-north-america-qualifiers-ro256/?game=all&tab=economy")

#utils.le_partidas("https://www.vlr.gg/300032/rose-vs-arkangel-esports-challengers-league-2024-north-america-qualifiers-ro128")

#utils.le_partidas("https://www.vlr.gg/280308/sengoku-gaming-vs-fav-gaming-predator-league-japan-2024-sf/?game=145294&tab=performance")

def minha_funcao():    
#     dataframe = pd.DataFrame(columns=[
#      'date', 'patch', 'nomePrimeiroTime', 'nomeSegundoTime',
#      'tipo_partida', 'mapas', 'rounds', 'estatisticas',
#      'quadro_all_kills', 'quadro_jogadas', 'quadro_compras',
#      'quadro_tipo_compra_por_round'
#     ])

    dados = utils.le_paginas(os.getenv("BASE_URL"), pagina_inicial=1, num_paginas=480, num_threads=10)


#     for registro in dados:
#          dataframe = dataframe.append(registro, ignore_index=True)
    

    dataframe = pd.DataFrame(data = dados)
    diretorio_atual = os.getcwd()
    
    caminho_arquivo_csv = os.path.join(diretorio_atual, "dados.csv")
    dataframe.to_csv(caminho_arquivo_csv, index=False)
    #dataframe.to_pickle(os.path.join(diretorio_atual, 'dados.pkl'))

#Chamada da função assim que o arquivo for executado
if __name__ == "__main__":
     minha_funcao()
