# #class BurroSimulation:
#     __init__():  # carga config, dijkstra, constelaciones
#     simulateRoute(start, end):  # ejecuta la simulación
#     calculateEnergy(distance):  # calcula energía consumida
#     eatGrass(star):  # aplica regeneración
#     updateHealth():  # cambia estado de salud
#     generateReport():  # crea el reporte final
from Back.Controller.ControllerConfig import ControllerConfig
from Back.Controller.ControllerConstellations import ControllerConstellations
from Back.utils.FlujoOptimo import dijkstra

class DonkeySimulation:
    def __init__(self):
        self.configDonkey = ControllerConfig()
        self.constellations = ControllerConstellations()
        self.dijkstra = dijkstra()
        self.dataConstellations = self.constellations.fetchJsonConstellations()
        self.configData = self.configDonkey.fetchConfig()
    
    def calculateDistance(self,start1,start2):
        data=self.dataConstellations
        start_a=self.constellations.fetchDistanceBetweenStars(start1)
        start_b=self.constellations.fetchDistanceBetweenStars(start2)
        if start_a is None or start_b is None:
            return None
        return start_a - start_b
       
        

    def simulateRoute(self, startStar, endStar):
        if not self.configData:
            return None
        result = self.dijkstra.flujoOptimo(startStar, endStar)
        if not result:
            return None
        
        route=result['path']
        totalDistance=result['distance']
        for i in range(len(route)-1):
            currentStar = route[i]
            nextStar= route[i + 1]

