class Stats():
    def __init__(self, matrizDesempenho):
        self.stats = {}
        self.economy = {}
        for jogador in matrizDesempenho:
            hashmap = {}
            hashmap["Nacionalidade"] = jogador[1]
            hashmap["Operador"] = jogador[2]
            hashmap["R"] = jogador[3]
            hashmap["ACS"] = jogador[4]
            hashmap["K"] = jogador[5]
            hashmap["D"] = jogador[6]
            hashmap["A"] = jogador[7]
            hashmap["KDA+/-"] = jogador[8]
            hashmap["KAST"] = jogador[9]
            hashmap["ADR"] = jogador[10]
            hashmap["HS%"] = jogador[11]
            hashmap["FK"] = jogador[12]
            hashmap["FD"] = jogador[13]
            hashmap["FKFD+/-"] = jogador[14]
            self.stats[jogador[0]] = hashmap # jogador[0] guarda o nome do jogador
        
    @property
    def stats(self):
        return self.stats

    @stats.setter
    def stats(self, value):
        self.stats = value
