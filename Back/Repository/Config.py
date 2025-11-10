import json
import os
from Back.models.Config import Config

class Config:
    """
    Config class for managing a JSON configuration file.
    This class encapsulates reading from, writing to, creating, and modifying a JSON
    configuration stored at self.RUTA_DE_CONFIGURACION (default "Back/Data/Config.json").
    Methods
    -------
    __init__():
        Initialize the Config instance and set the default path to the JSON file.
    readJsonConfig():
        Read and parse the JSON configuration file.
        - Returns: A Python object (typically a dict or list) parsed from JSON, or
          None if the file does not exist or is empty.
        - Notes: This method will propagate JSON parsing errors (json.JSONDecodeError)
          and file I/O errors if they occur.
    saveConfig(data):
        Serialize and write the supplied Python object to the configuration file as JSON.
        - Parameters:
            data: The Python object (dict, list, etc.) to be saved to disk.
        - Side effects: Overwrites the file at self.RUTA_DE_CONFIGURACION with
          the JSON representation of `data` using an indentation of 4 spaces.
        - Notes: May raise I/O related exceptions (e.g., OSError) on failure.
    createConfig(config):
        Create or append a configuration entry.
        - Parameters:
            config: An object expected to implement a `toDict()` method that returns
                    a serializable dictionary representation.
        - Behavior: If the configuration file is missing or empty, a new list is
          initialized. Otherwise, the existing JSON (expected to be a list) is loaded,
          the new dictionary is appended, and the resulting list is saved back to disk.
        - Notes: Assumes the stored JSON is a list of entries. May raise exceptions
          related to JSON parsing or file I/O. The provided `config.toDict()` must
          return a JSON-serializable structure.
    modifyConfig(newBurroEnergiaIcial, newEstadoSalud, newPasto, newNumber, newStartAge, newDeathAge):
        Modify the existing configuration dictionary with new values for specific keys.
        - Parameters:
            newBurroEnergiaIcial: Value to set for the 'burroEnergiaIcial' key.
            newEstadoSalud: Value to set for the 'estadoSalud' key.
            newPasto: Value to set for the 'pasto' key.
            newNumber: Value to set for the 'number' key.
            newStartAge: Value to set for the 'startAge' key.
            newDeathAge: Value to set for the 'deathAge' key.
        - Behavior: If the configuration file does not exist or is empty, the method
          prints a message and returns without making changes. Otherwise, it loads
          the configuration (expected to be a dict), updates the listed keys, and
          saves the updated dict back to disk.
        - Notes: The method assumes the top-level JSON structure is a dictionary.
          JSON parsing and I/O errors may be raised by underlying operations.
    General Notes
    -------------
    - The class does not perform strict type validation on values written to the
      configuration; callers should ensure values are JSON-serializable and of the
      expected types.
    - File existence and emptiness checks are used to decide whether to read or
      initialize configuration data. Invalid JSON content will raise standard JSON
      parsing exceptions.
    """
    def __init__(self):
        self.RUTA_DE_CONFIGURACION = "Back/Data/Config.json"
    
    def readJsonConfig(self):
        if not os.path.exists(self.RUTA_DE_CONFIGURACION) or os.path.getsize(self.RUTA_DE_CONFIGURACION) == 0:
            print("No hay datos existentes dentro de archivo")
            return None
        else:
            with open(self.RUTA_DE_CONFIGURACION, 'r') as file:
                configData = json.load(file)
                return configData
    
    def saveConfig(self,data):
        with open(self.RUTA_DE_CONFIGURACION, 'w') as file:
            json.dump(data, file, indent=4)
    
    def createConfig(self,config):
        newConfig = config.toDict()
        if not os.path.exists(self.RUTA_DE_CONFIGURACION) or os.path.getsize(self.RUTA_DE_CONFIGURACION) == 0:
            config=[]
        else:
            with open(self.RUTA_DE_CONFIGURACION, 'r') as file:
                config = json.load(file)
        config.append(newConfig)
        self.saveConfig(newConfig)
    
    def modifyConfig(self,newBurroEnergiaIcial,newEstadoSalud,newPasto,newNumber,newStartAge,newDeathAge):
        if not os.path.exists(self.RUTA_DE_CONFIGURACION) or os.path.getsize(self.RUTA_DE_CONFIGURACION) == 0:
            print("No hay configuración para modificar.")
            return
        else:
            configData = self.readJsonConfig()
            if configData:
                configData['burroEnergiaIcial'] = newBurroEnergiaIcial
                configData['estadoSalud'] = newEstadoSalud
                configData['pasto'] = newPasto
                configData['number'] = newNumber
                configData['startAge'] = newStartAge
                configData['deathAge'] = newDeathAge
            self.saveConfig(configData)


            
