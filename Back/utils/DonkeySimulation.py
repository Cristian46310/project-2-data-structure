import random
from Back.Controller.ControllerConfig import ControllerConfig
from Back.Controller.ControllerConstellations import ControllerConstellations
from Back.utils.FlujoOptimo import dijkstra

class DonkeySimulation:
    """
    DonkeySimulation
    High-level simulation manager for a "donkey" that travels between stars, consumes energy
    and grass, ages over distance traveled, and can be affected by random diseases or
    special star types (hypergiants). This class coordinates configuration, constellation
    data and a Dijkstra pathfinder to run route simulations and update persistent config.
    Dependencies / Expected environment:
    - ControllerConfig: provides fetchConfig() and modifyConfig(...) for persistent donkey config.
    - ControllerConstellations: provides fetchJsonConstellations(), fetchDistanceBetweenStars(a, b),
        and fetchTimeToEatGrassService(star).
    - dijkstra: provides flujoOptimo(start, end) -> {'path': [...], 'distance': total_distance}
    - random module is used in validateDiases for probabilistic disease selection.
    Configuration structure expected from ControllerConfig.fetchConfig():
    {
            'burroEnergiaIcial': float,   # initial energy percent (0-100)
            'startAge': float,            # starting "age" or life-years
            'deathAge': float,            # age at which the donkey dies
            'pasto': float,               # available grass (kg)
            'estadoSalud': str,           # health state string, e.g. "excelente" / "regular" / ...
            'number': Any                 # auxiliary identifier persisted by modifyConfig
    Public Methods
    --------------
    __init__():
            Initialize internal helpers and fetch configuration and constellation data.
            Side effects: constructs ControllerConfig, ControllerConstellations and dijkstra instances
            and reads their data into self.configData and self.dataConstellations.
    calculateDistance(start1, start2):
            Return the distance between two stars using the constellations service.
            Parameters:
                    start1 (str): label/name of the first star
                    start2 (str): label/name of the second star
            Returns:
                    float or None: distance between stars, or None if not available.
    calculateEnergy(distance):
            Compute energy lost when traveling a given distance.
            Parameters:
                    distance (float): distance traveled
            Returns:
                    float: energy lost (distance * 0.3)
    eatGrass(grass, donkeyEnergy, stateHealth, timeToEatGrass):
            Simulate the donkey eating grass to regain energy.
            Parameters:
                    grass (float): available grass in kg before eating
                    donkeyEnergy (float): current energy percent (0-100)
                    stateHealth (str): health state affecting energy recovery ("excelente", "regular", others)
                    timeToEatGrass (float): time units available to eat (affects kg consumed; 1 kg per time unit)
            Returns:
                    tuple: (newEnergy: float, remainingGrass: float)
            Notes:
                    - If donkeyEnergy >= 50 or no grass available, returns inputs unchanged.
                    - Grass consumed = min(grass, timeToEatGrass * 1).
                    - Energy gained per kg depends on stateHealth:
                            - "excelente": +10 energy per kg
                            - "regular": +6 energy per kg
                            - otherwise: +4 energy per kg
                    - Energy is clamped at 100.
                    - Prints progress and amount eaten as side effects.
    lifeDonkeyDistance(star1, star2):
            Search the constellation dataset for stars and compute the donkey's life after
            traveling the distance between star1 and star2 if both are found in the same constellation.
            Parameters:
                    star1 (str), star2 (str): labels of the two stars to find
            Returns:
                    float or None: updated lifeYears (startAge + distance) if both stars found and life < deathAge,
                                                 prints death message and returns None if life >= deathAge or required data missing.
            Notes:
                    - Uses internal self.dataConstellations and self.configData.
                    - If constellation/config data is missing, returns None.
    research(mission):
            Perform mission-related checks and possibly trigger disease validation or simple energy changes.
            Parameters:
                    mission (str): one of 'exploración', 'recoleccion', 'transporte', 'entretención', 'dormir' (case-insensitive)
            Returns:
                    - If mission is exploration / recoleccion / transporte: returns the result of validateDiases()
                        (may be a tuple describing a disease or a health string).
                    - If 'entretención': returns configData['startAge'] + 10 (energy-like value).
                    - If 'dormir': returns configData['startAge'] + 20.
            Side effects:
                    - Prints short messages for some mission types.
    validateDiases():
            Randomly determine whether the donkey has a disease and, if so, select one and
            return its severity and life impact.
            Returns:
                    - If no disease: returns the string 'El burro está saludable'.
                    - If disease: returns a tuple (healthState: str, lifeLost: int, diseaseName: str)
                        where healthState is one of 'bien', 'regular', 'deplorable', 'grave'.
            Behavior:
                    - Uses random.choices with approximate 30% chance of disease.
                    - Disease-to-lifeLost mapping:
                            'Constipación Cósmica' -> 5
                            'Radiación Galáctica Aguda' -> 20
                            'Síndrome del Casco Atascado' -> 10
                            'Neuralgia del Cometa' -> 30
            Side effects:
                    - Prints whether a disease was detected.
    hypergiant(starName, nextGalaxy, nextStar, energy, grass):
            If the current star is marked as a hypergiant in the constellation data, apply special
            energy and grass multipliers and validate the existence of a destination star in the provided galaxy.
            Parameters:
                    starName (str): label of the current star
                    nextGalaxy (str): name of the target galaxy/constellation to search for the destination star
                    nextStar (str): label of the intended next star within nextGalaxy
                    energy (float): current energy value
                    grass (float): current grass amount
            Returns:
                    tuple (newEnergy: float, newGrass: float) if hypergiant effect applies and destination exists,
                    otherwise None.
            Effects:
                    - If star is hypergiant: energy increases by 50% and grass is doubled before checking destination.
                    - Only returns values if the destination star exists in nextGalaxy.
    validateEnergy(energy):
            Clamp energy into the inclusive range [0, 100].
            Parameters:
                    energy (float)
            Returns:
                    float: clamped energy value
    simulateRoute(startStar, endStar, constellation, nextStarInNewGalaxy, mission):
            Simulate the donkey traversing an optimal route found by the dijkstra component,
            handling energy consumption, grass-eating, disease checks, potential hypergiant jumps,
            life progression and persisting updated config.
            Parameters:
                    startStar (str): starting star label
                    endStar (str): destination star label
                    constellation (str): name of the constellation/galaxy used for hypergiant destination checks
                    nextStarInNewGalaxy (str): destination star label in the next galaxy used by hypergiant()
                    mission (str): mission type passed to research()
            Returns:
                    dict or None:
                            If successful, returns a dict:
                            {
                                    "route": [...],            # list of star labels visited
                                    "distanceTotal": float,    # total distance returned by dijkstra
                                    "energyFinal": float,      # final clamped energy
                                    "lifeFinal": float,        # final lifeYears
                                    "status": "Vivo"|"Muerto"
                            If required data or pathfinder result missing, returns None.
            Behavior and side effects:
                    - Obtains route and total distance from self.dijkstra.flujoOptimo(startStar, endStar).
                    - Initializes local state from self.configData:
                            energy <- 'burroEnergiaIcial'
                            life   <- 'startAge'
                            deathAge <- 'deathAge'
                            grass <- 'pasto'
                            healthState <- 'estadoSalud'
                    - Iterates each hop in the route:
                            - Decreases energy by calculateEnergy(distance between current and next).
                            - Increments life by the same distance.
                            - Computes time to eat grass from constellation service, adjusts it, and calls eatGrass()
                                if energy < 50.
                            - Calls research(mission); if it returns a disease tuple, applies lifeLost to life and updates healthState.
                            - Checks hypergiant() to possibly alter energy/grass and perform an intergalactic validation.
                            - If life >= deathAge or energy <= 0 the loop breaks and the donkey is considered dead.
                    - After the route, energy is clamped via validateEnergy().
                    - Calls self.configDonkey.modifyConfig(...) to persist mutated values:
                            newBurroEnergiaIcial, newEstadoSalud, newPasto, newNumber, newStartAge, newDeathAge
                    - Prints progress messages during the simulation.
            Notes:
                    - The method relies on side-effecting prints and persistent config modifications.
                    - The sign convention for life progression uses distance as additional "age" units.
                    - Energy and life may be increased by disease (lifeLost) or hypergiant effects.
    """
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
        if donkeyEnergy >= 50 or grass <= 0:
            return donkeyEnergy, grass 

        grassConsumed = min(grass, timeToEatGrass * 1)  

        if stateHealth.lower() == "excelente":
            donkeyEnergy += grassConsumed * 10
        elif stateHealth.lower() == "regular":
            donkeyEnergy += grassConsumed * 6
        else:
            donkeyEnergy += grassConsumed * 4

        donkeyEnergy = min(donkeyEnergy, 100)
        print(donkeyEnergy)  
        grass -= grassConsumed  

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
            if isinstance(diseaseResult, tuple):
                healthState, lifeLost, diseaseName = diseaseResult
                life += lifeLost
                print(f"El burro contrajo {diseaseName}. Estado de salud: {healthState}. Tiempo de vida afectado: {lifeLost} años luz.")
            else:
                print("No se detectaron enfermedades.")

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



