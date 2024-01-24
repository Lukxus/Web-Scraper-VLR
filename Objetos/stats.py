class stats():
    def __init__(self, matrizDesempenho):
        self.stats = {}
        self.economy = {}
        for jogador in matrizDesempenho:
            hashmap = {}
            hashmap["Operador"] = jogador[1]
            hashmap["R"] = jogador[2]
            hashmap["ACS"] = jogador[3]
            hashmap["K"] = jogador[4]
            hashmap["D"] = jogador[5]
            hashmap["A"] = jogador[6]
            hashmap["KDA+/-"] = jogador[7]
            hashmap["KAST"] = jogador[8]
            hashmap["ADR"] = jogador[9]
            hashmap["HS%"] = jogador[10]
            hashmap["FK"] = jogador[11]
            hashmap["FD"] = jogador[12]
            hashmap["FKFD+/-"] = jogador[13]
            self.stats[jogador[0]] = hashmap # jogador[0] guarda o nome do jogador
        
    @property
    def stats(self):
        return self.stats

    @stats.setter
    def stats(self, value):
        self.stats = value
