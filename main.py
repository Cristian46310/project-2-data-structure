from Back.Repository.Config import Config as ConfigRepo
from Back.models.Config import Config


repo = ConfigRepo()

repo.modifyConfig(
    newBurroEnergiaIcial=150,
    newSalud=90,
    newEstadoSalud="Bueno",
    newPasto=250,
    newNumber=321,
    newStartAge=15,
    newDeathAge=4000
)


config_modificada = repo.readJsonConfig()
print(config_modificada)