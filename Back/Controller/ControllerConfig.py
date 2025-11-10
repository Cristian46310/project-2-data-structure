from Back.Services.ServiceConfig import ServiceConfig

class ControllerConfig:
    """
    ControllerConfig
    Controller responsible for delegating configuration-related operations to a ServiceConfig backend.
    Attributes
    ----------
    service : ServiceConfig
        Instance of the service that implements configuration retrieval, creation, and modification.
    Methods
    -------
    __init__()
        Initialize the controller and create its ServiceConfig dependency.
    fetchConfig() -> Any
        Retrieve the current configuration via the service.
        Returns
        -------
        Any
            The configuration object as returned by ServiceConfig.getConfig() (commonly a dict or domain model).
    createConfig(config: Any) -> None
        Create a new configuration by delegating to the service.
        Parameters
        ----------
        config : Any
            Configuration data to be created (a dict, DTO, or model accepted by the service).
        Raises
        ------
        Exception
            Propagates any exceptions raised by ServiceConfig.createConfig (e.g., validation or persistence errors).
    modifyConfig(newBurroEnergiaIcial: Union[int, float], newEstadoSalud: Any, newPasto: Any, newNumber: int, newStartAge: int, newDeathAge: int) -> None
        Update configuration values by delegating to the service.
        Parameters
        ----------
        newBurroEnergiaIcial : int | float
            New initial energy value for the entity (numeric).
        newEstadoSalud : Any
            New health/state value (string or domain-specific type).
        newPasto : Any
            New pasture identifier or configuration for pasture (string or domain type).
        newNumber : int
            New number/count value.
        newStartAge : int
            New starting age value.
        newDeathAge : int
            New death/maximum age value.
    """
    def __init__(self):
        self.service = ServiceConfig()
    
    def fetchConfig(self):
        return self.service.getConfig()
    
    def createConfig(self, config):
        self.service.createConfig(config)
    
    def modifyConfig(self, newBurroEnergiaIcial,  newEstadoSalud, newPasto, newNumber, newStartAge, newDeathAge):
        self.service.modifyConfig(newBurroEnergiaIcial,  newEstadoSalud, newPasto, newNumber, newStartAge, newDeathAge)