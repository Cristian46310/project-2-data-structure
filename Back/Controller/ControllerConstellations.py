from Back.Services.SerivceReadConstellations import ServiceReadConstellations

class ControllerConstellations:
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
    
    def fetchDistanceBetweenStars(self, start1):
        return self.service.getDistanceBetweenStars(start1)
