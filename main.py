from Back.utils.DonkeySimulation import DonkeySimulation
from Back.Repository.ReadConstellations import ReadConstellations
from Back.Controller.ControllerConstellations import ControllerConstellations

controleer=ControllerConstellations()
starA = 'Beta178'
starB = 'Gama23'  

# Bloquear el camino
# controleer.setConnectionStatus(starA, starB, True)

controleer.setConnectionStatus(starA, starB, False)








