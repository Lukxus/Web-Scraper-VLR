
import Objetos.stats as stats
import economy
import performace

class partida():
    def __init__(
            self,
            nomePrimeiroTime,
            nomeSegundoTime,
            rounds, #Uma lista de enums criada pela função tranforma_rounds
            mapa,
            matrizStatsPrimeiroTime,
            matrizStatsSegundoTime,
            matrizeconomiaPrimeiroTime,
            matrizeconomiaSegundoTime,
            matrizDesempenhoPrimeiroTime,
            matrizDesempenhoSegundoTime,
            
            dataPartida #trabalhar com um tipo de data
            ):
        self.nomePrimeiroTime = nomePrimeiroTime
        self.nomeSegundoTime = nomeSegundoTime
        self.rounds = rounds
        self.mapa = mapa
        self.statsPrimeiroTime = stats(matrizStatsPrimeiroTime)
        self.statsSegundoTime = stats(matrizStatsSegundoTime)

        self.economiaPrimeiroTime = economy(matrizeconomiaPrimeiroTime)
        self.economiaSegundoTime = economy(matrizeconomiaSegundoTime)

        self.statsPrimeiroTime = performace(matrizDesempenhoPrimeiroTime)
        self.statsSegundoTime = performace(matrizDesempenhoSegundoTime)

        self.dataPartida = dataPartida
        

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
        self._stats_primeiro_time = stats(value)

    @property
    def stats_segundo_time(self):
        return self._stats_segundo_time

    @stats_segundo_time.setter
    def stats_segundo_time(self, value):
        self._stats_segundo_time = stats(value)

    @property
    def data_partida(self):
        return self._data_partida

    @data_partida.setter
    def data_partida(self, value):
        self._data_partida = value
