import json
import os

class ReadConstellations:
    """"
    ReadConstellations
    A helper class for reading and manipulating constellation data stored in a JSON file.
    Attributes
    - RUTA_DE_CONSTELACIONES (str): Path to the JSON file containing constellation data. Default: "back/Data/Constellations.json".
    Behavior overview
    - This class provides methods to load the JSON file, list constellations and their stars,
        query star attributes and links, compute distances between connected stars, and enable/disable
        individual links. Most read methods return None if the underlying JSON file is missing,
        empty, or if a requested item cannot be found.
    - The method setConnectionStatus modifies the JSON structure in memory and persists changes
        back to the same file when any update is made.
    Notes and side effects
    - All methods assume the JSON structure contains a top-level "constellations" array. Each
        constellation is expected to contain at least the keys "name" and "starts" (an array of star objects).
    - Star objects are expected to contain fields such as "id", "label", "timeToEat", "amountOfEnergy",
        and "linkedTo" (an array of link objects). Link objects are expected to contain "starId",
        "distance" and optionally "blocked".
    - readJsonConstellations uses file system operations and JSON parsing. Malformed JSON, missing
        permissions, or file-system errors will raise built-in exceptions (e.g., OSError, JSONDecodeError)
        from the underlying libraries.
    - setConnectionStatus writes updated JSON back to RUTA_DE_CONSTELACIONES when an update occurs.
        Calling code should ensure concurrent access is handled appropriately (this class does not perform locking).
    Public methods (summary)
    - readJsonConstellations() -> dict | None
            Load and return the parsed JSON content. Returns None and prints a message if the file does not exist
            or is empty.
    - allConstellations() -> list[str] | None
            Return a list of constellation names extracted from the JSON, or None if the JSON cannot be loaded.
    - findStartsInConstellation(constellationName: str) -> list[str] | None
            Given a constellation name, return a list of star labels for that constellation, or None if not found.
    - linksWithStars(constellationName: str) -> list[list[dict]] | None
            Return the raw "linkedTo" lists for every star in the named constellation (i.e., a list where each element
            is the "linkedTo" array of a star). Returns None if JSON cannot be loaded or the constellation is absent.
    - findStartByIdAndName(id, constellationName: str) -> str | None
            Find a star by its id within the specified constellation and return its label. Returns None if not found.
    - splitConstellattionsLinks(constellationName: str) -> list[tuple] | None
            Flatten the link structures for a constellation into a list of tuples (starId, distance).
            Returns None if JSON cannot be loaded or the constellation is absent.
    - ReadNameStarById(id) -> str | None
            Search all constellations for a star with the given id and return its label, or None if not found.
    - readDistanceBetweenStars(start_label: str, end_label: str) -> (int|float) | None
            Search for a direct link from a star with label start_label to a linked star matching end_label.
            If found return the link's "distance"; otherwise return None.
    - readTimeToEatGrass(star_label: str) -> (int|float) | None
            Return the "timeToEat" property for a star with the specified label, or None if not found.
    - readAmountOfEnergy(star_label: str) -> (int|float) | None
            Return the "amountOfEnergy" property for a star with the specified label, or None if not found.
            This method also prints the energy value as a side effect.
    - setConnectionStatus(starA_label: str, starB_label: str, enabled: bool) -> bool
            Enable or disable the connection between two stars by updating their corresponding link objects'
            "blocked" property. Parameter enabled maps to the stored "blocked" flag as:
                enabled=True  -> link['blocked'] = False
                enabled=False -> link['blocked'] = True
            The method updates both directions when present. If any changes were made the JSON file is rewritten.
            Returns True if any link was updated; otherwise False.
    Example usage
            rc = ReadConstellations()
            all_names = rc.allConstellations()
            stars = rc.findStartsInConstellation("Orion")
            dist = rc.readDistanceBetweenStars("Betelgeuse", "Rigel")
            success = rc.setConnectionStatus("StarA", "StarB", enabled=False)
    Exceptions
    - The class methods intentionally return None (or False for setConnectionStatus) for many "not found"
        conditions. However, file I/O and JSON parsing still propagate underlying exceptions (e.g., OSError,
        PermissionError, json.JSONDecodeError). Caller code should catch these where appropriate.
    Limitations
    - No validation is performed on the JSON schema beyond simple key accesses; unexpected structures may
        raise exceptions.
    - There is no concurrency control for simultaneous reads/writes to the JSON file.
        """
    def __init__(self):
        self.RUTA_DE_CONSTELACIONES = "back/Data/Constellations.json"
        # Construir ruta absoluta al JSON en Back/Data independientemente del working dir
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Data'))
        self.RUTA_DE_CONSTELACIONES = os.path.join(base_dir, 'Constellations.json')
        # fallback (mantener compatibilidad) si por algún motivo no existe
        if not os.path.exists(self.RUTA_DE_CONSTELACIONES):
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









