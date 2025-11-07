import json
import os
from Back.models.Config import Config

class Config:
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


            
