from Back.Repository.ReadConstellations import ReadConstellations as Constellations

class ServiceReadConstellations:
    """
    ServiceReadConstellations
    Service layer that exposes read and light-management operations for constellation
    and star data by delegating to an underlying Constellations repository instance.
    This class acts as a thin wrapper around repository methods, providing a stable
    interface for higher-level application code (controllers, handlers, tests) while
    keeping data-access concerns encapsulated in the repository.
    Attributes:
        repository (Constellations): The repository instance used to perform all data
            retrieval and update operations.
    Methods:
        getAllConstellations() -> Any
            Return all constellations available from the repository. The exact return
            type depends on the repository implementation (commonly a list or dict).
        getStarsInConstellation(constellationName: str) -> Any
            Retrieve the stars that belong to the given constellation name.
        getLinksWithStars(constellationName: str) -> Any
            Retrieve link/edge information for the specified constellation, typically
            connecting stars within that constellation.
        getStarByIdAndName(id, constellationName) -> Any
            Find and return a star by its identifier and the constellation name it
            belongs to. Returns repository-specific representation (e.g., dict) or
            None if not found.
        getSplitConstellationsLinks(constellationName: str) -> Any
            Return split/parsed link data for a constellation. Useful when links are
            stored as concatenated strings and need to be split into structured records.
        getJsonConstellations() -> Any
            Read and return constellation data in JSON-compatible form from the
            repository (e.g., parsed JSON structure).
        getStarNameById(id) -> str | None
            Return the human-readable name/label of a star given its identifier, or
            None if the id is not present.
        getDistanceBetweenStars(start1, start2) -> float | Any
            Compute or retrieve the distance between two stars identified by the
            provided parameters. The numeric type and units depend on repository
            semantics.
        readTimeToEatGrass(starLabel) -> Any
            Read and return a time-related metric associated with the star identified
            by starLabel. The semantics (units, type) depend on repository data.
        readAmountOfEnergy(starLabel) -> Any
            Read and return an energy-related metric for the star identified by
            starLabel.
        readTimeToEatGrassService(starLabel) -> Any
            Alias for readTimeToEatGrass; preserved for backward compatibility or
            naming convenience.
        manageConnection(starA, starB, enabled: bool) -> Any
            Enable or disable a connection (edge) between two stars. Returns the
            repository operation result (commonly a boolean success flag or updated
            record).
    Example:
        service = ServiceReadConstellations()
        constellations = service.getAllConstellations()
        stars = service.getStarsInConstellation("Orion")
    """
    def __init__(self):
        self.repository = Constellations()
    
    def getAllConstellations(self):
        return self.repository.allConstellations()
    
    def getStarsInConstellation(self, constellationName):
        return self.repository.findStartsInConstellation(constellationName)
    
    def getLinksWithStars(self, constellationName):
        return self.repository.linksWithStars(constellationName)
    
    def getStarByIdAndName(self, id, constellationName):
        return self.repository.findStartByIdAndName(id, constellationName)
    
    def getSplitConstellationsLinks(self, constellationName):
        return self.repository.splitConstellattionsLinks(constellationName)
    
    def getJsonConstellations(self):
        return self.repository.readJsonConstellations()
    
    def getStarNameById(self, id):
        return self.repository.ReadNameStarById(id)
    
    def getDistanceBetweenStars(self, start1,start2):
        return self.repository.readDistanceBetweenStars(start1,start2)
    
    def readTimeToEatGrass(self, starLabel):
        return self.repository.readTimeToEatGrass(starLabel)
    
    def readAmountOfEnergy(self, starLabel):
        return self.repository.readAmountOfEnergy(starLabel)
    
    def readTimeToEatGrassService(self, starLabel):
        return self.repository.readTimeToEatGrass(starLabel)
    
    def manageConnection(self, starA, starB,enabled):
        return self.repository.setConnectionStatus(starA, starB, enabled)
    
    