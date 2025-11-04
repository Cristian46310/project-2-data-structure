from Back.Repository.Config import Config

class ServiceConfig:
    def __init__(self):
        self.configRepo = Config()
    
    def getConfig(self):
        return self.configRepo.readJsonConfig()
    
    def createConfig(self,config):
        self.configRepo.createConfig(config)
    
    def modifyConfig(self,newBurroEnergiaIcial,newSalud,newEstadoSalud,newPasto,newNumber,newStartAge,newDeathAge):
        self.configRepo.modifyConfig(newBurroEnergiaIcial,newSalud,newEstadoSalud,newPasto,newNumber,newStartAge,newDeathAge)
        