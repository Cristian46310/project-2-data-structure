class Config:
    def __init__(self, burroEnergiaIcial,salud,estadoSalud,pasto,number,startAge,deathAge):
        self.burroEnergiaIcial = burroEnergiaIcial
        self.salud = salud
        self.estadoSalud = estadoSalud
        self.pasto = pasto
        self.number = number
        self.startAge = startAge
        self.deathAge = deathAge
    
    def toDict(self):
        return {
            "burroEnergiaIcial": self.burroEnergiaIcial,
            "salud": self.salud,
            "estadoSalud": self.estadoSalud,
            "pasto": self.pasto,
            "number": self.number,
            "startAge": self.startAge,
            "deathAge": self.deathAge
        }