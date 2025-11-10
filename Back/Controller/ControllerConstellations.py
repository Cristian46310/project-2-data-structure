from Back.Services.SerivceReadConstellations import ServiceReadConstellations

class ControllerConstellations:
    """
    ControllerConstellations
    Facade-style controller that delegates constellation- and star-related operations
    to an underlying ServiceReadConstellations instance.
    This class provides simple fetch and manage methods used by higher-level
    components (for example, a web API or UI layer) to retrieve constellation data,
    star details, connections between stars, and computed metrics such as distance,
    energy amounts, and time-to-eat-grass estimates.
    Attributes
    ----------
    service : ServiceReadConstellations
        The service instance responsible for performing data access and business
        logic. All controller methods forward their work to corresponding service
        methods.
    Public Methods
    --------------
    fetchAllConstellations()
        Return a collection of all constellations available from the service.
    fetchStarsInConstellation(constellationName)
        Return the stars that belong to the constellation named by `constellationName`.
    fetchLinksWithStars(constellationName)
        Return link information (edges/connections) for the specified constellation,
        optionally including associated star information.
    fetchStarByIdAndName(id, constellationName)
        Return details for the star identified by `id` within the constellation
        named `constellationName`.
    fetchSplitConstellationsLinks(constellationName)
        Return a split or partitioned representation of links for the given
        constellation (e.g., separate lists of nodes and edges or connected
        components), as provided by the service.
    fetchJsonConstellations()
        Return a JSON-serializable representation (or JSON string) of all
        constellations; useful for APIs or exports.
    fetchStarNameById(id)
        Return the label or name of the star identified by `id`.
    fetchDistanceBetweenStars(start1, start2)
        Return the computed distance (numeric) between two stars identified by
        `start1` and `start2` (identifiers, labels or objects as accepted by the service).
    fetchTimeToEatGrass(starLabel)
        Return the time estimate related to "time to eat grass" for the star whose
        label is `starLabel`. The exact unit and semantics are determined by the service.
    fetchAmountOfEnergy(starLabel)
        Return the amount of energy associated with the star identified by `starLabel`.
    fetchTimeToEatGrassService(starLabel)
        Variant read method that forwards to a differently named service function;
        retains the same purpose as fetchTimeToEatGrass but may call a distinct
        backend implementation.
    setConnectionStatus(starA, starB, enabled)
        Enable or disable the connection between `starA` and `starB`. Returns the
        result of the service operation (e.g., success flag or updated connection info).
    """
    def __init__(self):
        self.service = ServiceReadConstellations()
    
    def fetchAllConstellations(self):
        return self.service.getAllConstellations()
    
    def fetchStarsInConstellation(self, constellationName):
        return self.service.getStarsInConstellation(constellationName)
    
    def fetchLinksWithStars(self, constellationName):
        return self.service.getLinksWithStars(constellationName)
    
    def fetchStarByIdAndName(self, id, constellationName):
        return self.service.getStarByIdAndName(id, constellationName)
    
    def fetchSplitConstellationsLinks(self, constellationName):
        return self.service.getSplitConstellationsLinks(constellationName)
    
    def fetchJsonConstellations(self):
        return self.service.getJsonConstellations()
    
    def fetchStarNameById(self, id):
        return self.service.getStarNameById(id)
    
    def fetchDistanceBetweenStars(self, start1,start2):
        return self.service.getDistanceBetweenStars(start1,start2)
    
    def fetchTimeToEatGrass(self, starLabel):
        return self.service.readTimeToEatGrass(starLabel)
    
    def fetchAmountOfEnergy(self, starLabel):
        return self.service.readAmountOfEnergy(starLabel)
    
    def fetchTimeToEatGrassService(self, starLabel):
        return self.service.readTimeToEatGrassService(starLabel)
    
    def setConnectionStatus(self, starA, starB, enabled):
        return self.service.manageConnection(starA, starB, enabled)
