import json
import os

class ReadConstellations:
    def __init__(self):
        self.RUTA_DE_CONSTELACIONES = "back/Data/Constellations.json"

    def readJsonConstellations(self):
        if not os.path.exists(self.RUTA_DE_CONSTELACIONES) or os.path.getsize(self.RUTA_DE_CONSTELACIONES) == 0:
            print("No hay datos existentes dentro de archivo")
            return None
        else:
            with open(self.RUTA_DE_CONSTELACIONES, 'r') as file:
                Constellations = json.load(file)
                return Constellations
    
    def allConstellations(self):
        constellationsJson = self.readJsonConstellations()
        if constellationsJson is None:
            return None
        else:
            constellations=[constellations['name'] for constellations in constellationsJson['constellations']]
            return constellations
    
    def findStartsInConstellation(self, constellationName):
        constellationsJson = self.readJsonConstellations()
        if constellationsJson is None:
            return None
        else:
            for constellation in constellationsJson['constellations']:
                if constellation['name'] == constellationName:
                    return [star['label'] for star in constellation['starts']]
        return None 
    
    def linksWithStars(self, constellationName):
        constellationsJson = self.readJsonConstellations()
        if constellationsJson is None:
            return None
        else:
            for constellation in constellationsJson['constellations']:
                if constellation['name'] == constellationName:
                    return [star['linkedTo'] for star in constellation['starts']]
        return None
    
    def findStartByIdAndName(self, id, constellationName):
        constellationsJson = self.readJsonConstellations()
        if constellationsJson is None:
            return None
        else:
            for constellation in constellationsJson['constellations']:
                if constellation['name'] == constellationName:
                    for star in constellation['starts']:
                        if star['id'] == id:
                            return star['label']
        return None
    
    def splitConstellattionsLinks(self, constellationName):
        split=self.linksWithStars(constellationName)
        if split is None:
            return None
        else:
            tuplaIdDistance=[]
            for list in split:
                for stars in list:
                    tuplaIdDistance.append((stars['starId'], stars['distance']))
            return tuplaIdDistance
    
    def ReadNameStarById(self, id):
        constellationsJson = self.readJsonConstellations()
        if constellationsJson is None:
            return None
        else:
            for constellation in constellationsJson['constellations']:
                for star in constellation['starts']:
                    if star['id'] == id:
                        return star['label']
        return None
    
    def readDistanceBetweenStars(self, start_label, end_label):
        constellationsJson = self.readJsonConstellations()
        if constellationsJson is None:
            return None

        for constellation in constellationsJson['constellations']:
            for star in constellation['starts']:
                if star['label'] == start_label:  # Origen
                    for link in star['linkedTo']:
                        linkedStarId = link['starId']
                        linkedStarName = self.ReadNameStarById(linkedStarId)
                        if linkedStarName == end_label:  # Destino
                            return link['distance']
        return None
    

    def readTimeToEatGrass(self, star_label):
        constellationsJson = self.readJsonConstellations()
        if constellationsJson is None:
            return None
        for constellation in constellationsJson['constellations']:
            for star in constellation['starts']:
                if star['label'] == star_label:
                    return star['timeToEat']
        return None
    
    def readAmountOfEnergy(self, star_label):
        constellationsJson = self.readJsonConstellations()
        if constellationsJson is None:
            return None
        for constellation in constellationsJson['constellations']:
            for star in constellation['starts']:
                if star['label'] == star_label:
                    print(star['amountOfEnergy'])
                    return star['amountOfEnergy']
        return None
    
    def setConnectionStatus(self, starA_label, starB_label, enabled):
        """
        Bloquea o habilita el camino entre dos estrellas.
        enabled=True -> habilitar (blocked=False)
        enabled=False -> bloquear (blocked=True)
        """
        constellationsJson = self.readJsonConstellations()
        if constellationsJson is None:
            return False

        updated = False
        for constellation in constellationsJson['constellations']:
            for star in constellation['starts']:
                if star['label'] == starA_label:
                    for link in star['linkedTo']:
                        linkedStarName = self.ReadNameStarById(link['starId'])
                        if linkedStarName == starB_label:
                            link['blocked'] = not enabled
                            updated = True
                if star['label'] == starB_label:
                    for link in star['linkedTo']:
                        linkedStarName = self.ReadNameStarById(link['starId'])
                        if linkedStarName == starA_label:
                            link['blocked'] = enabled
                            updated = True

        if updated:
            with open(self.RUTA_DE_CONSTELACIONES, 'w') as file:
                json.dump(constellationsJson, file, indent=4)
        return updated









