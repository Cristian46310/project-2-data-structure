from Back.Repository.Config import Config

class ServiceConfig:
    """
    ServiceConfig
    Service layer that delegates configuration persistence operations to an underlying
    Config repository instance.
    This class wraps a Config repository (expected to provide readJsonConfig,
    createConfig and modifyConfig methods) and exposes simple methods to get,
    create, and modify application configuration.
    Attributes:
        configRepo: Instance of the Config repository used for all I/O operations.
    Methods:
        getConfig() -> Any
            Retrieve and return the current configuration as provided by the
            repository's readJsonConfig() method.
        createConfig(config: dict) -> None
            Persist a new configuration. The `config` argument is passed through
            to the repository's createConfig() method.
        modifyConfig(newBurroEnergiaIcial, newEstadoSalud, newPasto, newNumber,
                     newStartAge, newDeathAge) -> None
            Update configuration fields by delegating to the repository's
            modifyConfig(...) method. Parameters correspond to the concrete fields
            expected by the repository; types and validation are handled by the
            repository implementation.
    """
    def __init__(self):
        self.configRepo = Config()
    
    def getConfig(self):
        return self.configRepo.readJsonConfig()
    
    def createConfig(self,config):
        self.configRepo.createConfig(config)
    
    def modifyConfig(self,newBurroEnergiaIcial,newEstadoSalud,newPasto,newNumber,newStartAge,newDeathAge):
        self.configRepo.modifyConfig(newBurroEnergiaIcial,newEstadoSalud,newPasto,newNumber,newStartAge,newDeathAge)
        
        