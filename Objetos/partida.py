#import Performace
import Objetos.Stats as Stats
#import Economy

class Partida():
    def __init__(
            self,
            nomePrimeiroTime,
            nomeSegundoTime,
            rounds, #Uma lista de enums criada pela função tranforma_rounds
            tipoPartida,
            mapa, #Lista de mapas
            matrizStatsPrimeiroTime,
            matrizStatsSegundoTime,
            matrizeconomiaPrimeiroTime,
            matrizeconomiaSegundoTime,
            matrizDesempenhoPrimeiroTime,
            matrizDesempenhoSegundoTime,
            dataPartida, #trabalhar com um tipo de data
            patch
            ):
        self.nomePrimeiroTime = nomePrimeiroTime
        self.nomeSegundoTime = nomeSegundoTime
        self.rounds = rounds
        self.tipoPartida = tipoPartida
        self.mapa = mapa
        self.statsPrimeiroTime = Stats(matrizStatsPrimeiroTime)
        self.statsSegundoTime = Stats(matrizStatsSegundoTime)

        # self.economiaPrimeiroTime = Economy(matrizeconomiaPrimeiroTime)
        # self.economiaSegundoTime = Economy(matrizeconomiaSegundoTime)

        # self.statsPrimeiroTime = Performace(matrizDesempenhoPrimeiroTime)
        # self.statsSegundoTime = Performace(matrizDesempenhoSegundoTime)

        self.dataPartida = dataPartida
        self.patch = patch
        

    @property
    def nome_primeiro_time(self):
        return self._nome_primeiro_time

    @nome_primeiro_time.setter
    def nome_primeiro_time(self, value):
        self._nome_primeiro_time = value

    @property
    def nome_segundo_time(self):
        return self._nome_segundo_time

    @nome_segundo_time.setter
    def nome_segundo_time(self, value):
        self._nome_segundo_time = value

    @property
    def rounds(self):
        return self._rounds

    @rounds.setter
    def rounds(self, value):
        self._rounds = value

    @property
    def mapa(self):
        return self._mapa

    @mapa.setter
    def mapa(self, mapa):
        self._mapa = mapa

    @property
    def stats_primeiro_time(self):
        return self._stats_primeiro_time

    @stats_primeiro_time.setter
    def stats_primeiro_time(self, value):
        self._stats_primeiro_time = Stats(value)

    @property
    def stats_segundo_time(self):
        return self._stats_segundo_time

    @stats_segundo_time.setter
    def stats_segundo_time(self, value):
        self._stats_segundo_time = Stats(value)

    @property
    def data_partida(self):
        return self._data_partida

    @data_partida.setter
    def data_partida(self, value):
        self._data_partida = value
    
    @property
    def patch(self):
        return self._patch

    @patch.setter
    def patch(self, value):
        self._patch = value
