from Back.Repository.ReadConstellations import ReadConstellations as Constellations

class ServiceReadConstellations:
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
    
    