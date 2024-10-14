import utils
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()


#https://www.vlr.gg/9398/reality-rift-vs-paper-rex-champions-tour-malaysia-singapore-stage-1-challengers-1-ro16
#https://www.vlr.gg/316456/dsyre-vs-vx300-gaming-challengers-league-2024-italy-rinascimento-split-1-playoffs-uf
#x = utils.le_partidas("https://www.vlr.gg/316456/dsyre-vs-vx300-gaming-challengers-league-2024-italy-rinascimento-split-1-playoffs-uf")
#print(len(x["estatisticas"]))


def minha_funcao():

    utils.limpa_arquivos(os.getenv("CAMINHO_ERROS_TXT"))
    utils.escreveHora(os.getenv("CAMINHO_ERROS_TXT"))
    dataframe = pd.DataFrame(
        columns=[
            "url",
            "campeonato"
            "date",
            "patch",
            "nomePrimeiroTime",
            "nomeSegundoTime",
            "tipo_partida",
            "mapas",
            "rounds",
            "estatisticas",
            "quadro_all_kills",
            "quadro_jogadas",
            "quadro_compras",
            "quadro_tipo_compra_por_round",
        ]
    )

    dados = utils.le_paginas(
        os.getenv("BASE_URL"), pagina_inicial=1, num_paginas=532, num_threads=12
    )
    print("_________________")
    print("Fim dos acessos")
    print("_________________")

    # for registro in dados:
    #     dataframe = dataframe.append(registro, ignore_index=True)

    dataframe = pd.DataFrame(data=dados)
    diretorio_atual = os.getcwd()

    caminho_arquivo_csv = os.path.join(diretorio_atual, os.getenv("CAMINHO_CSV"))
    caminho_arquivo_pickle = os.path.join(diretorio_atual, os.getenv("CAMINHO_PICKLE"))
    caminho_arquivo_JSON = os.path.join(diretorio_atual, os.getenv("CAMINHO_JSON"))

    dataframe.to_pickle(caminho_arquivo_pickle)
    dataframe.to_csv(caminho_arquivo_csv, index=False)
    dataframe.to_json(caminho_arquivo_JSON, orient="records")

    utils.escreveHora(os.getenv("CAMINHO_ERROS_TXT"))


# Chamada da função assim que o arquivo for executado
if __name__ == "__main__":
    minha_funcao()
