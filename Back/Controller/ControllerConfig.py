from Back.Services.ServiceConfig import ServiceConfig

class ControllerConfig:
    def __init__(self):
        self.service = ServiceConfig()
    
    def fetchConfig(self):
        return self.service.getConfig()
    
    def createConfig(self, config):
        self.service.createConfig(config)
    
    def modifyConfig(self, newBurroEnergiaIcial,  newEstadoSalud, newPasto, newNumber, newStartAge, newDeathAge):
        self.service.modifyConfig(newBurroEnergiaIcial,  newEstadoSalud, newPasto, newNumber, newStartAge, newDeathAge)