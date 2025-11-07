import random
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
        distance=self.constellations.fetchDistanceBetweenStars(start1,start2)
        return distance
    
    def calculateEnergy(self, distance):
        energyLost=distance*0.3
        return energyLost
    



    def eatGrass(self, grass, donkeyEnergy, stateHealth, timeToEatGrass):
        """
        Aplica regeneración de energía del burro al comer pasto.
        Retorna:
        energy -> energía actualizada
        grass -> pasto restante
        """
        if donkeyEnergy >= 50 or grass <= 0:
            return donkeyEnergy, grass  # No necesita comer o no hay pasto

        # Cantidad de pasto que puede comer según el tiempo de estancia
        grassConsumed = min(grass, timeToEatGrass * 1)  # 1 kg por unidad de tiempo

        # Aumenta energía según estado de salud se reajustaron los valores por la gran caida de la energia al hacer los calculos
        if stateHealth.lower() == "excelente":
            donkeyEnergy += grassConsumed * 10
        elif stateHealth.lower() == "regular":
            donkeyEnergy += grassConsumed * 6
        else:
            donkeyEnergy += grassConsumed * 4

        donkeyEnergy = min(donkeyEnergy, 100)
        print(donkeyEnergy)  # Limita energía al máximo
        grass -= grassConsumed  # Reduce el pasto disponible

        print(f"El burro come {grassConsumed} kg de pasto, energía: {donkeyEnergy}%")

        return donkeyEnergy, grass
                
    def lifeDonkeyDistance(self,star1,star2):
        donkey=self.configData  
        array=[]
        lifeYears=donkey['startAge']
        deathAge=['deathAge']
        constellations=self.dataConstellations
        if not self.constellations or not self.configData:
            return None
        else:
            for constellation in constellations['constellations']:
                for stars in constellation['starts']:
                    array.append(stars["label"])
                if(star1 in array and star2 in array):
                    distanceStars=self.calculateDistance(star1,star2)
                    reducedLive=lifeYears+distanceStars
                    if reducedLive>=deathAge:
                        print('El burro ha muerto')
                        #funcion del sonido del burro
                    else:
                        return reducedLive
                array = []
    

    def research(self,mission):
        if(mission.lower()=='exploración'):
            disease=self.validateDiases()       
            return disease
        if(mission.lower()=='recoleccion'):
            disease=self.validateDiases()
            print("El burro está recolectando muestras")
            return disease
        if (mission.lower()=='transporte'):
            disease=self.validateDiases()
            print("El burro está transportando materiales")
            return disease
        if (mission.lower()=='entretención'):
            energia=self.configData['startAge']+10
            return energia
        if (mission.lower()=='dormir'):
            energia=self.configData['startAge']+20
            return energia

        
               
    def validateDiases(self):
        diseases = ["Constipación Cósmica", "Radiación Galáctica Aguda", "Síndrome del Casco Atascado", "Neuralgia del Cometa"]
        has_disease = random.choices([True, False], weights=[0.3, 0.7], k=1)[0]
        print("¿El burro tiene alguna enfermedad?", has_disease)
        if not has_disease:
            return 'El burro está saludable'
        else:
            lifeLost=0
            donkeyDease = random.choice(diseases)
            if donkeyDease == 'Constipación Cósmica':
                lifeLost=5
                return 'bien', lifeLost,donkeyDease
            if donkeyDease == 'Radiación Galáctica Aguda':
                lifeLost=20
                return 'deplorable', lifeLost,donkeyDease
            if donkeyDease == 'Síndrome del Casco Atascado':
                lifeLost=10
                return 'regular', lifeLost,donkeyDease
            if donkeyDease == 'Neuralgia del Cometa':
                lifeLost=30
                return 'grave', lifeLost,donkeyDease
            return donkeyDease
    
    def hypergiant(self, starName, nextGalaxy, nextStar, energy, grass):
        contellationsJson = self.dataConstellations
        # Verifica si la estrella actual es hipergigante
        is_hypergiant = False
        for constellation in contellationsJson['constellations']:
            for star in constellation['starts']:
                if star['label'] == starName and star.get('hypergiant', False):
                    is_hypergiant = True
                    break
            if is_hypergiant:
                break
        if is_hypergiant:
            energy += energy * 0.50
            grass *= 2
            # Verifica que el destino exista en la siguiente galaxia
            for constellation in contellationsJson['constellations']:
                if constellation['name'] == nextGalaxy:
                    for star in constellation['starts']:
                        if star['label'] == nextStar:
                            return energy, grass
        return None
    
    def validateEnergy(self, energy):
        if energy > 100:
            return 100
        if energy < 0:
            return 0
        return energy
    
    def simulateRoute(self, startStar, endStar, constellation, nextStarInNewGalaxy, mission):
        if not self.configData:
            return None
        result = self.dijkstra.flujoOptimo(startStar, endStar)
        if not result:
            return None
        route = result['path']
        totalDistance = result['distance']
        energy = self.configData['burroEnergiaIcial']
        life = self.configData['startAge']
        deathAge = self.configData['deathAge']
        grass = self.configData['pasto']
        healthState = self.configData['estadoSalud']
        number = self.configData['number']

        for i in range(len(route) - 1):
            currentStar = route[i]
            nextStar = route[i + 1]
            print(f"Visitando {currentStar} → Próxima: {nextStar}")
            distance = self.calculateDistance(currentStar, nextStar)
            if distance is None:
                continue
            energy -= self.calculateEnergy(distance)
            life += distance
            timeAtStar = self.constellations.fetchTimeToEatGrassService(currentStar)
            timeAtStar= timeAtStar*2
            timeToEatGrass = timeAtStar/2
            if energy < 50:
                grassConsumed = min(grass, timeToEatGrass * 1)
                print(f"Energía {energy}% — el burro come pasto en {currentStar}.")
                energy, grass = self.eatGrass(grass, energy, healthState, timeToEatGrass)

            diseaseResult = self.research(mission)
            #isInstace: verifica si lo que nos devuelve el metodo es una tupla (valor, tipo de dato)
            if isinstance(diseaseResult, tuple):
                healthState, lifeLost, diseaseName = diseaseResult
                life += lifeLost
                print(f"El burro contrajo {diseaseName}. Estado de salud: {healthState}. Tiempo de vida afectado: {lifeLost} años luz.")
            else:
                print("No se detectaron enfermedades.")

            # Salto intergaláctico si corresponde
            hyper = self.hypergiant(currentStar, constellation, nextStarInNewGalaxy, energy, grass)
            if hyper:
                energy, grass = hyper
                print(f"Salto intergaláctico: energía {energy}, pasto {grass}")

            if life >= deathAge or energy <= 0:
                print(" El burro ha muerto.")
                healthState = 'Muerto'
                break
        energy = self.validateEnergy(energy)
        self.configDonkey.modifyConfig(
            newBurroEnergiaIcial=energy,
            newEstadoSalud=healthState,
            newPasto=grass,
            newNumber=number,
            newStartAge=life,
            newDeathAge=deathAge
        )
        return {
            "route": route,
            "distanceTotal": totalDistance,
            "energyFinal": energy,
            "lifeFinal": life,
            "status": "Muerto" if life >= deathAge or energy <= 0 else "Vivo"
        }



